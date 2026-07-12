# src/utils/pay.py
import random
import datetime
import hashlib
from decouple import config
import httpx


def generate_out_trade_no():
    # 1. 使用原生 Python 获取当前时间字符串
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # 2. 生成随机数
    random_str = str(random.randint(100000, 999999))
    return f"{now_str}{random_str}"


class VPay:
    def __init__(self):
        self.api_url = config("V_API_URL")
        self.key = config("V_KEY")
        self.notifyUrl = config("NOTIFY_URL")
        self.returnUrl = self.notifyUrl

    def create_sign(self, payId, param, type, price, reallyPrice=""):
        # md5(payId+param+type+price+通讯密钥)
        sign_str = f"{payId}{param}{type}{price}{reallyPrice}{self.key}"
        sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
        return sign

    def sign_verify(self, params: dict, sign_str):
        # md5(payId + param + type + price + reallyPrice + 通讯密钥)
        payId = params.get("payId")
        param = params.get("param")
        type = params.get("type")
        price = params.get("price")
        reallyPrice = params.get("reallyPrice")

        sign = self.create_sign(payId, param, type, price, reallyPrice)

        if sign != sign_str:
            return False

        return True

    def generate_orderId(self, payId, type, price, param=""):
        # type参数 微信支付传入1 支付宝支付传入2
        sign = self.create_sign(payId, param, type, price)
        payload = {
            "payId": payId,
            "type": type,
            "price": price,
            "sign": sign,
            "param": param,
            "isHtml": 0,
            "notifyUrl": self.notifyUrl,
            "returnUrl": self.returnUrl,
        }
        response = httpx.post(self.api_url + "createOrder", data=payload, timeout=10)
        return response.json()["data"]["orderId"]

    def get_payUrl(self, orderId):
        Pay_Url = self.api_url + "payPage/pay.html?orderId=" + orderId
        return Pay_Url
