# import manage_list, search, util
import functions_framework
from flask import make_response

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
    return "Hello Request"