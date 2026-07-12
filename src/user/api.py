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

api = Router()
# auth_api = Router()


### 普通用户 ###
# @auth_api.post("login", response={200: TokenSchema, 400: dict})
# def login(request, payload: LoginSchema):
#     user = get_object_or_404(User, username=payload.username)
#     if not user.check_password(payload.password):
#         raise HttpError(400, "账号或密码错误")
#     token = create_token(user)
#     return {"access_token": token}


# @auth_api.post("register")
# def register(request, payload: RegisterSchema):
#     if (
#         User.objects.filter(username=payload.username).exists()
#         or User.objects.filter(email=payload.email).exists()
#     ):
#         raise HttpError(400, "账号已存在")
#     user = User.objects.create_user(**payload.model_dump(exclude='password2'))

#     return {"detail": "注册成功"}


# @auth_api.post("reset-password", auth=AuthBearer())
# def reset_password(request, payload: ResetPasswordSchema):
#     user = request.auth
#     if not user.check_password(payload.old_password):
#         raise HttpError(400, "旧密码错误")

#     user.set_password(payload.new_password)
#     user.save()
#     return {"detail": "密码修改成功"}


### 以下是通用格式 ###
db_model = User


@api.post("/", response=out_model)
def create(request, payload: create_model):
    if (
        User.objects.filter(username=payload.username).exists()
        or User.objects.filter(email=payload.email).exists()
    ):
        raise HttpError(400, "账号创建失败")
    return db_model.objects.create(**payload.model_dump())


@api.get("/", response=list[out_model])
@paginate(CustomPagination)
def list_data(request, filters: Query[filter_model]):
    querysets = db_model.objects.all()
    querysets = filters.filter(querysets)
    return querysets


@api.get("/{id}", response=out_model)
def detail_data(request, id: int):
    return get_object_or_404(db_model, id=id)


@api.put("/{id}", response=out_model)
def update_data(request, id: int, payload: update_model):
    data = get_object_or_404(db_model, id=id)

    updates = payload.model_dump(exclude_unset=True)
    for attr, value in updates.items():
        setattr(data, attr, value)
    data.save()
    return data


@api.delete("/{id}")
def delete_data(request, id: int):
    data = get_object_or_404(db_model, id=id)
    data.delete()
    return {"detail": "删除成功"}
