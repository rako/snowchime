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
    
    stripped_data = input_data
    
    return stripped_data


# チャンネルIDが存在しているかチェック

def check_channel_id(data):
    # urlであった場合、チャンネルIDを取得する
    sanitized_data = validate_input(data)
    
    if len(sanitized_data) >= 1:
        return True
    else:
        return False