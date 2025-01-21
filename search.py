import json, os
from apiclient.discovery import build

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


# APIを作成する
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


# 検索クエリを作成する
channel_url = "https://www.youtube.com/channel/"


# APIに検索をかける
def search(data):
    response = youtube.search().list(
        part = "snippet",
        type = "channel",
        q = channel_url + data
    ).execute()