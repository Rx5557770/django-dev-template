# src/utils/captcha.py
from ninja import Router
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

api = Router()


@api.get("/captcha", summary="获取验证码")
def get_captcha(request):
    # 1. 在数据库中生成一条随机的验证码记录
    hashkey = CaptchaStore.generate_key()
    # 2. 根据这个 key，获取生成图片的相对 URL (形如 /captcha/image/xxxx/)
    image_url = captcha_image_url(hashkey)

    # 3. 把完整的图片路径和 hashkey 返回给前端
    # 提示：如果是生产环境，前端需要拼接上服务端的域名，例如: f"https://api.yourdomain.com{image_url}"
    return {"captcha_key": hashkey, "captcha_image": image_url}
