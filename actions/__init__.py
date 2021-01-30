from actions.conversion import resize, svg_to_jpg
from utils.sqs import SQS
import json


async def process_msg(api: str, payload: any, meta):
    try:
        if api == 'resize':
            await resize(payload)
        elif api == 'svg_to_png':
            await svg_to_jpg(payload)
        else:
            raise Exception(f'Invalid API {str}')
    except Exception as e:
        await SQS().send_to_error_queue(e, json.dumps(
            {'api': api, 'payload': payload}))  # send to error queue for replay once issue is resolved
        print('Handled exception', e)  # print exception
