# src/user/api.py
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ninja import Router, Query
from ninja.pagination import paginate
from ninja.errors import HttpError

from .schemas import (
    TokenSchema,
    UserCreateSchema as create_model,
    UserUpdateSchema as update_model,
    UserOutSchema as out_model,
    UserFilterSchema as filter_model,
    LoginSchema,
    RegisterSchema,
    ResetPasswordSchema,
)
from src.utils.pagination import CustomPagination
from src.auth.auth import AuthBearer
from src.utils.jwt import create_token

User = get_user_model()

private_api = Router()
public_api = Router()


### 普通用户 ###
@public_api.post("login", response={200: TokenSchema, 400: dict})
def login(request, payload: LoginSchema):
    user = User.objects.filter(username=payload.username).first()
    if not user:
        raise HttpError(400, "账号或密码错误")
    if not user.check_password(payload.password):
        raise HttpError(400, "账号或密码错误")
    token = create_token(user)
    if not token:
        raise HttpError(400, "账号状态异常")
    return {"access_token": token}


@public_api.post("register")
def register(request, payload: RegisterSchema):
    if (
        User.objects.filter(username=payload.username).exists()
        or User.objects.filter(email=payload.email).exists()
    ):
        raise HttpError(400, "账号已存在")
    user = User.objects.create_user(**payload.model_dump(exclude="password2"))

    return {"detail": "注册成功"}


@public_api.post("reset-password", auth=AuthBearer())
def reset_password(request, payload: ResetPasswordSchema):
    user = request.auth
    if not user.check_password(payload.old_password):
        raise HttpError(400, "旧密码错误")

    user.set_password(payload.new_password)
    user.save()
    return {"detail": "密码修改成功"}


### 以下是通用格式 ###
db_model = User


@private_api.post("/", response=out_model)
def create(request, payload: create_model):
    if (
        User.objects.filter(username=payload.username).exists()
        or User.objects.filter(email=payload.email).exists()
    ):
        raise HttpError(400, "账号创建失败")
    return db_model.objects.create(**payload.model_dump())


@private_api.get("/", response=list[out_model])
@paginate(CustomPagination)
def list_data(request, filters: Query[filter_model]):
    querysets = db_model.objects.all()
    querysets = filters.filter(querysets)
    return querysets


@private_api.get("/{id}", response=out_model)
def detail_data(request, id: int):
    return get_object_or_404(db_model, id=id)


@private_api.put("/{id}", response=out_model)
def update_data(request, id: int, payload: update_model):
    data = get_object_or_404(db_model, id=id)

    updates = payload.model_dump(exclude_unset=True)
    for attr, value in updates.items():
        setattr(data, attr, value)
    data.save()
    return data


@private_api.delete("/{id}")
def delete_data(request, id: int):
    data = get_object_or_404(db_model, id=id)
    data.delete()
    return {"detail": "删除成功"}
