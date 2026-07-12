# src/router/api.py
from ninja import NinjaAPI, Router
from decouple import config

from src.auth.auth import AdminBearer
from src.user.api import private_api as user_private_api, public_api as user_public_api

api = NinjaAPI()
admin_api = Router()
api.add_router("admin", admin_api, auth=AdminBearer())

# 验证码
if config("CAPTCHA", cast=bool):
    from src.utils.captcha import api as captcha_api

    api.add_router("captcha", captcha_api, tags=["Captcha"])

### 管理员接口 ###
admin_api.add_router("users", user_private_api, tags=["Private-Users"])


### 公开接口 ###
api.add_router("users", user_public_api, tags=["Public-Users"])
