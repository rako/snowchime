import manage_list, search, util
import functions_framework

@functions_framework.http
def main(request):
    # 購読確認リクエスト処理
    if "hub.mode" in request.args and request.args["hub.mode"] == "subscribe":
        if "hub.challenge" in request.args:
            return Response(status=200, body=request.challenge)
        else:
            return Response(status=500)
    
    # 実際のリクエスト処理
    return Response(status=200)