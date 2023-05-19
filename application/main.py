import os
import sys

import aiohttp

from fastapi import Request, FastAPI, HTTPException

from linebot import (
    AsyncLineBotApi, WebhookParser
)
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction
)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

app = FastAPI()
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
line_bot_api = AsyncLineBotApi(channel_access_token, async_http_client)
parser = WebhookParser(channel_secret)

@app.post("/")
async def main(request: Request):

    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = await request.body()
    body = body.decode()

    print("body : "+body)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        await line_bot_api.reply_message(
            event.reply_token,
            # TextSendMessage(text=event.message.text)
            # TextSendMessage(text="who are you?")
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    thumbnail_image_url='https://drive.google.com/uc?id=1qkEQ_chWbedwqACad7bTmrb7-GagOX_B',
                    title='Menu',
                    text='Please select',
                    actions=[
                        PostbackAction(
                            label='postback',
                            display_text='postback text',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='message',
                            text='message text'
                        ),
                        URIAction(
                            label='uri',
                            uri='http://example.com/'
                        )
                    ]
                )
            )
        )

    return 'OK'