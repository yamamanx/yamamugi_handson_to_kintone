
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

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def post_record(record_dict):
    response = None
    try:
        data = {'app': kintone_app}
        data['record'] = record_dict
        response = requests.post(
            post_url,
            data=json.dumps(data),
            headers=headers
        )
        return json.loads(response.text)['id']
    except Exception as e:
        logger.error(response.text)
        logger.error(traceback.format_exc())


def lambda_handler(event, context):

    try:
        phone_number = event['phone_number']
        line_code = event['line_code']

        insert_record = {}
        insert_record['phone_number'] = {'value': phone_number}
        insert_record['line_code'] = {'value': line_code}

        record_no = post_record(insert_record)
        response_url = KINTONE_RESPONSE_URL.format(
            kintone_domain=kintone_domain,
            app=kintone_app,
            record_no=str(record_no)
        )

        return {'kintone_url': response_url}

    except Exception as e:
        logger.error(traceback.format_exc())
        raise(traceback.format_exc())
