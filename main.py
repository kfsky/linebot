from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi('35F33AoMvSMrROjy3XOXQ+Wr6kDjo03e7P+OTqRtC3jKLpGVrxYeXY4kBI7d8liX8G1zZoZm6FjQzaub0yXxq+MLC5eZXH5to+sxNRMfHJvlpFDoeRAcKYHRCrv52HqpLtDmU06HkoYqYTmOc0fEjgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a008bc253cdb2a5ab7136d75cad3834e')


@app.route("/")
def hello_world():
    return "hello world!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
