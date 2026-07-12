# src/utils/pagination.py
from typing import Any
from pydantic import Field

from ninja import Schema
from ninja.pagination import PaginationBase


class CustomPagination(PaginationBase):
    # only `skip` param, defaults to 5 per page
    class Input(Schema):
        skip: int = Field(default=0, ge=0)  # 跳过多少项
        limit: int = Field(ge=0, le=20, default=20)  # 每页显示最大数量

    class Output(Schema):
        items: list[Any]  # `items` is a default attribute
        total: int
        limit: int
        skip: int

    def paginate_queryset(self, queryset, pagination: Input, **params):

        skip = pagination.skip
        limit = pagination.limit
        return {
            "items": queryset[skip : skip + limit],
            "total": queryset.count(),
            "limit": limit,
            "skip": skip,
        }
