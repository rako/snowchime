# import manage_list, search, util
import functions_framework
from flask import make_response
import os
import discord
import requests, json

discord_token = os.environ.get("DISCORD_TOKEN")
discord_channel = os.environ.get("DISCORD_CHANNEL_ID")
client_id = os.environ.get("DISCORD_CLIENT_ID")
client_secret = os.environ.get("DISCORD_CLIENT_SECRET")

webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

@functions_framework.http
def main(request):
    # 購読確認リクエスト処理
    if "hub.mode" in request.args and request.args["hub.mode"] == "subscribe":
        challenge = request.args.get("hub.challenge")
        if challenge:
            response = make_response(challenge)
            response.headers["Content-Type"] = "text/plain"
            response.status_code = 200
            return response
        else:
            response = make_response("Invalid request", 400)
            return response
    
    # 実際のリクエスト処理
    send_message()
    return "OK"


def send_message():
    main_content = {
        'content': 'test text'
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(webhook_url, data=json.dumps(main_content), headers=headers)