import requests

url = "https://asia-northeast2-sound-bee-448211-m4.cloudfunctions.net/snowchime"

with open("test_xml.xml", "r", encoding="utf-8") as file:
    xml_content = file.read()

def test():
    headers = {
        "Content-Type": "application/atom+xml"
    }
    response = requests.post(url, headers=headers, data=xml_content)
    
    # デバッグ用
    print(response.text)
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {response.text}")

test()