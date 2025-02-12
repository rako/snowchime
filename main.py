# import manage_list, search, util

import functions_framework
import os
import requests
from flask import Response
import xml.etree.ElementTree as ET

discord_token = str(os.environ.get("DISCORD_TOKEN"))
discord_channel = int(os.environ.get("DISCORD_CHANNEL_ID"))
# client_id = int(os.environ.get("DISCORD_CLIENT_ID"))
# client_secret = str(os.environ.get("DISCORD_CLIENT_SECRET"))

discord_api_url = f"https://discord.com/api/v10/channels/{discord_channel}/messages"

@functions_framework.http
def main(request):
    # 購読確認リクエスト処理
    if "hub.mode" in request.args and request.args["hub.mode"] == "subscribe":
        challenge = request.args.get("hub.challenge")
        response = Response()
        if challenge:
            response.set_data(challenge)
            response.mimetype = "text/plain"
            response.status = 200
            return response
        else:
            response.set_data("Invalid request")
            response.status = 400
            return response
    
    # 実際のリクエスト処理
    if request.method == "POST" and request.host_url == "https://pubsubhubbub.appspot.com":
        send_message(request)
        return "sent"

    return "OK"


def send_message(request):
    headers = {
        "Authorization": f"Bot {discord_token}",
        "Content-Type": "application/json"
    }

    xmltree = ET.parse(request.get_data())
    root = xmltree.getroot()
    entry = root["entry"]

    # フィードの要素の時だけにする
    if root.tag != "feed":
        return

    published_date = entry.findtext("published")
    updated_date = entry.findtext("updated")
    video_title = entry.findtext("title")
    video_url = entry.findtext("link/@href")
    
    # 動画アップロードしたときだけにする
    #if published_date != updated_date:
        #return
    
    main_content = {
        "mention_everyone": True,
        "content": "新しい動画です！",
        "channel_id": discord_channel,
        "embeds": [
            {
                "title": video_title,
                "url": video_url,
            }
        ],
    }

    response = requests.post(discord_api_url, headers=headers, json=main_content)