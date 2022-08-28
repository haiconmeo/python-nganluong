from nganluong import NganLuong
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
app = FastAPI()

nganluong = NganLuong(
    merchant_site_code='',
    secure_pass='64cca435e30497c8cb989ca46077ca12',
    return_url='http://localhost:8000/payment_return',
    receiver='hoanghuumanh54@gmail.com',
    cancel_url='http://localhost:8000/payment_return',
    api_url='https://sandbox.nganluong.vn:8088/nl35/checkout.php'
)


@app.get("/payment")
def read_root():
    req = {
        'transaction_info': 'vantest',
        'order_code': 'NL_1447474310',
        'price': 2000,
        'currency': 'vnd',
        'quantity': 1,
        'tax': 0,
        'discount': 0,
        'fee_cal': 0,
        'fee_shipping': 0,
        'order_description': 'vantest',
        'buyer_info': None,
        'affiliate_code': None,
        'lang': 'vi',
        'cancel_url' :'http://localhost'
    }
    return RedirectResponse(nganluong.get_payment_url(req))


@app.get("/payment_return")
def read_item(request: Request):
    data = request.query_params.items()
    response = {}
    for i in data:
        response[i[0]] = i[1]
    if nganluong.validate_response(response):
        return "Thành công"
    else:
        return "Thất bại"
