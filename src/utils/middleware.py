# src/utils/middleware.py
import json
from django.utils.deprecation import MiddlewareMixin


class NinjaResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        content_type = response.get("Content-Type", "")
        # 非json数据，放行
        if not content_type.startswith("application/json"):
            return response

        # 不是api接口，放行
        if not request.path.startswith("/api/"):
            return response

        # 文档，放行
        if request.path.endswith(("/docs", "/openapi.json", "/redoc")):
            return response

        # 封装api响应
        try:
            orig_data = json.loads(response.content.decode("utf-8"))
            wrapped_data = {
                "code": response.status_code,
                "status": ("success" if 200 <= response.status_code < 300 else "error"),
                "data": orig_data,
            }
            response.content = json.dumps(wrapped_data, ensure_ascii=False).encode(
                "utf-8"
            )
            response["Content-Type"] = "application/json; charset=utf-8"
            response["Content-Length"] = str(len(response.content))
        except Exception:
            pass

        return response
