# src/router/api.py
from ninja import NinjaAPI
from decouple import config

from src.user.api import api as user_api

api = NinjaAPI()
# 验证码
if config("CAPTCHA", cast=bool):
    from src.utils.captcha import api as captcha_api

    api.add_router("captcha", captcha_api, tags=["Captcha"])


api.add_router("users", user_api, tags=["Users"])
