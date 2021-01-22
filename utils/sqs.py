import asyncio
import aiobotocore
from utils.config import Config
import json
from contextlib import AsyncExitStack
import logging


class SQS:
    queue_urls = {}
    client = None

    async def boot(self, exit_stack: AsyncExitStack, session: aiobotocore.session.AioSession):
        self.client = await exit_stack.enter_async_context(session.create_client('sqs'))
        for queue_name in Config.AWS.SQS_QUEUES:
            response = await self.client.create_queue(QueueName=queue_name)
            self.queue_urls[queue_name] = response['QueueUrl']
        print(self.queue_urls)

    def get_queue_url(self, queue_name):
        if self.queue_urls[queue_name] is None:
            raise Exception('Queue not found')
        return self.queue_urls[queue_name]

    async def send_message(self, queue_name, api, msg, meta=None):
        if meta is None:
            meta = {'attempt': 0}
        msg_body = {
            'api': api,
            'msg': msg,
            'meta': meta,
        }
        await self.client.send_message(QueueUrl=self.get_queue_url(queue_name), MessageBody=json.dumps(msg_body))

    async def send_to_error_queue(self, e: Exception, payload: str):
        msg_body = {
            'api': 'error',
            'msg': payload,
            'exception': str(e)
        }
        await self.client.send_message(QueueUrl=self.get_queue_url(Config.AWS.ERROR_QUEUE),
                                       MessageBody=json.dumps(msg_body))

    async def consume_messages(self, queue_name: str, max_number_of_messages=10):
        try:
            response = await self.client.receive_message(
                QueueUrl=self.get_queue_url(queue_name),
                MaxNumberOfMessages=max_number_of_messages,
                WaitTimeSeconds=2,
            )
            messages = []
            delete_messages_tasks = []
            if 'Messages' in response:
                for msg in response['Messages']:
                    try:
                        messages.append(json.loads(msg['Body']))
                        delete_messages_tasks.append(self.client.delete_message(
                            QueueUrl=self.get_queue_url(queue_name),
                            ReceiptHandle=msg['ReceiptHandle']
                        ))
                    except Exception as e:
                        logging.error(e)
            await asyncio.gather(*delete_messages_tasks)
            return messages
        except Exception as e:
            logging.error(e)

