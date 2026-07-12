# src/user/schemas.py
from pydantic import Field, EmailStr, model_validator
from ninja import Schema, FilterSchema, ModelSchema
from django.contrib.auth import get_user_model

User = get_user_model()
username_field = Field(..., min_length=6, max_length=150)
password_field = Field(..., min_length=6, max_length=128)


class TokenSchema(Schema):
    token_type: str = "bearer"
    access_token: str = Field(...)


### 普通用户操作 ###
class LoginSchema(Schema):
    username: str = username_field
    password: str = password_field


class RegisterSchema(ModelSchema):
    email: EmailStr
    password2: str = Field(..., max_length=128, exclude=True)

    @model_validator(mode="after")
    def check_password(self):
        if self.password != self.password2:
            raise ValueError("两次密码不一致")
        return self

    class Meta:
        model = User
        fields = ["username", "password", "email"]


class ResetPasswordSchema(Schema):
    old_password: str = password_field
    new_password: str = password_field


### 管理员 ###
class UserCreateSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class UserUpdateSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        fields_optional = "__all__"


class UserFilterSchema(FilterSchema):
    username: str | None = None
    email: EmailStr | None = None


class UserOutSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "is_staff"]
