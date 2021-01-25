import asyncio
from utils.sqs import SQS
from utils.config import Config
import aiobotocore
from contextlib import AsyncExitStack
import actions


async def run():
    session = aiobotocore.session.AioSession()
    async with AsyncExitStack() as exit_stack:
        sqs = SQS()
        await sqs.boot(exit_stack, session)

        for i in range(15):
            await sqs.send_message(Config.MEDIA.SQS_QUEUE, 'some_api', {'msg': f'some_msg:{i}'}, {'attempt': 1})

        # Workers consume and process messages
        while True:
            messages = await sqs.consume_messages(Config.MEDIA.SQS_QUEUE)
            if len(messages) == 0:
                await asyncio.sleep(1000)
                continue
            tasks = []
            for data in messages:
                tasks.append(actions.process_msg(data['api'], data['msg'], data['meta']))
            await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(run(), debug=True)
