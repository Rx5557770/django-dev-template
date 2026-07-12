# src/auth/auth.py
import jwt

from django.conf import settings
from django.contrib.auth import get_user_model

from ninja.security import HttpBearer
from ninja.errors import HttpError

User = get_user_model()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "token已过期")
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise HttpError(401, "请求失败")
        return user


class AdminBearer(AuthBearer):
    def authenticate(self, request, token):
        user = super().authenticate(request, token)

        # 非管理员用户时跳出
        if not (user.is_staff and user.is_active):
            raise HttpError(403, "Permission denied")

        # 管理员用户时返回用户信息
        return user
