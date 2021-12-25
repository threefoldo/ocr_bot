import os, sys
import hashlib
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.requests import Request
from wechat_sdk import WechatBasic
from wechat_sdk.messages import TextMessage, ImageMessage


token = os.environ.get('WECHAT_TOKEN')
wc = WechatBasic(token)
app = FastAPI()


@app.get('/')
async def WeChat(signature: str = Query(...),
        timestamp: str = Query(...),
        nonce: str = Query(...),
        echostr: str = Query(...)):
    if not signature:
        return JSONResponse('invalid request')
    params = [token, timestamp, nonce]
    params.sort()
    info = ''.join(params)
    sha1 = hashlib.sha1()
    sha1.update(info.encode())
    hcode = sha1.hexdigest()
    if hcode == signature:
        return PlainTextResponse(echostr)
    return ''



@app.post('/')
async def create_wechat(request: Request):
    body_text = await request.body()
    wc.parse_data(body_text)
    response = None
    msg = wc.get_message()
    if isinstance(msg, TextMessage):
        response = wc.response_text('text')
    elif isinstance(msg, ImageMessage):
        response = wc.response_text('image')

    return response



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app='service:app', host='0.0.0.0', port=8080, reload=True)
