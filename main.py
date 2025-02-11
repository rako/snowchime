# import manage_list, search, util
import functions_framework
import os
import discord
import requests, json

discord_token = str(os.environ.get("DISCORD_TOKEN"))
discord_channel = int(os.environ.get("DISCORD_CHANNEL_ID"))
client_id = int(os.environ.get("DISCORD_CLIENT_ID"))
client_secret = str(os.environ.get("DISCORD_CLIENT_SECRET"))

discord_api_url = f"https://discord.com/api/v10/channels/{discord_channel}/messages"

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
    if request.method == "POST":
        send_message()
        return "OK", 200


def send_message():
    main_content = {
        'content': 'test text'
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bot " + discord_token
    }

    response = requests.post(discord_api_url, headers=headers, json=main_content)