### チャンネルを管理する

# 入力チェック

def validate_url_input(input_data):
    if 'https://www.youtube.com/channel/' in input_data or 'https://www.youtube.com/@' in input_data or 'https://www.youtube.com/c/' in input_data:
        return True
    
    if input_data:
        return True
    
    return False


# チャンネルIDが存在しているかチェック

def check_channel_id():
    pass


# チャンネルを追加する

def add():
    if validate_url_input() == False:
        pass
    pass


# チャンネルを削除する

def delete():
    pass


# チャンネルを表示する

def display():
    pass