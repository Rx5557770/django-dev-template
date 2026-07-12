# src/utils/jwt.py
import jwt
from django.utils import timezone
from django.conf import settings


def create_token(user):
    token_payload = {
        "user_id": user.id,
        "exp": timezone.now() + timezone.timedelta(hours=1),
    }
    token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm="HS256")
    return token
