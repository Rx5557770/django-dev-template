# apps/account/schemas.py
from pydantic import Field, EmailStr, model_validator
from ninja import Schema, FilterSchema, ModelSchema
from django.contrib.auth import get_user_model

User = get_user_model()


class TokenSchema(Schema):
    token_type: str = "bearer"
    access_token: str = Field(...)


### 普通用户操作 ###
class LoginSchema(Schema):
    username: str
    password: str


class RegisterSchema(ModelSchema):
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
    old_password: str
    new_password: str


### 管理员 ###
class UserAdminCreateSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "password"]


class UserAdminUpdateSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "email", "password", "is_active"]
        fields_optional = "__all__"


class UserFilterSchema(FilterSchema):
    username: str | None = None
    email: EmailStr | None = None


class UserAdminOutSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "last_login", "date_joined"]


class UserPublicOutSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active", "last_login", "date_joined"]
