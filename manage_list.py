### チャンネルを管理する

# チャンネルリスト
channel_list = []

# 入力チェック

def validate_input(input_data):
    input_data = input_data.strip()
    stripped_data = ""

    if 'https://www.youtube.com/channel/' in input_data:
        stripped_data = input_data.replace('https://www.youtube.com/channel/', '')
    if 'https://www.youtube.com/@' in input_data:
        stripped_data = input_data.replace('https://www.youtube.com/@', '')
    if 'https://www.youtube.com/c/' in input_data:
        stripped_data = input_data.replace('https://www.youtube.com/c/', '')
    
    return stripped_data


# チャンネルIDが存在しているかチェック

def check_channel_id(data):
    # urlであった場合、チャンネルIDを取得する
    sanitized_data = validate_input(data)
    if len(sanitized_data) >= 1:
        search(data)
        return True
    else:
        return False


# APIに検索をかける
def search(data):
    pass


# チャンネルを追加する

def add():
    while(True):
        print("チャンネルIDを入力してください")
        data = input()
        # ここに"loading..."みたいなの入れてみる？
        if check_channel_id(data):
            channel_list.append(data)
            print("チャンネルが通知リストに追加されました")
            break
        print("そのようなチャンネルIDは存在しません")


# チャンネルを削除する

def delete():
    channel_list.remove()


# チャンネルを表示する

def display():
    print(channel_list)