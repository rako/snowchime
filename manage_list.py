### チャンネルを管理する

from search   import search
from util import validate_input, check_channel_id

# チャンネルリスト
channel_list = []


# チャンネルを追加する

def add():
    while(True):
        print("チャンネルIDを入力してください")
        data = input()
        # ここに"loading..."みたいなの入れてみる？
        if check_channel_id(data):
            if search(data) == True:
                channel_list.append(data)
                print("チャンネルが通知リストに追加されました")
                break
            else:
                print("そのようなチャンネルIDは存在しません")
        else:
            print("チャンネルIDもしくはチャンネルのURLを正しく入力してください")


# チャンネルを削除する

def delete():
    channel_list.remove()


# チャンネルを表示する

def display():
    print(channel_list)