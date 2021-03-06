
import requests
import json
import os
import logging
import traceback


kintone_app = os.environ['KINTONE_APP']
kintone_domain=os.environ['KINTONE_DOMAIN']

KINTONE_SINGLE_URL = "https://{kintone_domain}/k/v1/record.json"
KINTONE_RESPONSE_URL = "https://{kintone_domain}/k/{app}/show#record={record_no}&mode=edit"

post_url = KINTONE_SINGLE_URL.format(kintone_domain=kintone_domain)
headers = {
    'X-Cybozu-API-Token': os.environ['KINTONE_TOKEN'],
    'Content-Type' : 'application/json'
}

log_level = os.environ.get('LOG_LEVEL', 'INFO')

logger = logging.getLogger()

if log_level == 'ERROR':
    logger.setLevel(logging.ERROR)
elif log_level == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def post_record(record_dict):
    response = None
    try:
        data = {'app': kintone_app}
        data['record'] = record_dict
        logger.debug(data)

        response = requests.post(
            post_url,
            data=json.dumps(data),
            headers=headers
        )
        logger.debug(response.text)

        return json.loads(response.text)['id']
    except Exception as e:
        logger.error(response.text)
        logger.error(traceback.format_exc())
        raise (traceback.format_exc())


def lambda_handler(event, context):

    try:
        logger.debug(event)
        phone_number = event.get('phone_number','')
        line_code = event.get('line_code','')
        text = event.get('text','')
        reply = event.get('reply','')

        logger.debug(phone_number)
        logger.debug(line_code)
        logger.debug(text)
        logger.debug(reply)

        if phone_number:
            media = 'tel'
        else:
            media = 'line'

        logger.debug(media)

        insert_record = {}
        insert_record['phone_number'] = {'value': phone_number}
        insert_record['line_code'] = {'value': line_code}
        insert_record['media'] = {'value': media}
        insert_record['text'] = {'value': text}
        insert_record['reply'] = {'value': reply}

        logger.debug(insert_record)

        record_no = post_record(insert_record)

        logger.debug(record_no)

        response_url = KINTONE_RESPONSE_URL.format(
            kintone_domain=kintone_domain,
            app=kintone_app,
            record_no=str(record_no)
        )

        logger.debug(response_url)

        return {'kintone_url': response_url}

    except Exception as e:
        logger.error(traceback.format_exc())
        raise(traceback.format_exc())
