# Django Dev Template

一个现代化的 Django 5.2 项目模板，集成 Django Ninja API 框架，支持快速开发生产级别的 Web 应用。

## 📋 项目概述

- **开发框架**: Django 5.2 + django-ninja
- **编程语言**: Python 3.12
- **依赖管理**: uv
- **部署方式**: Docker + Docker Compose
- **数据库**: SQLite (开发) / MySQL (生产)
- **API 文档**: 自动生成 Swagger/OpenAPI 文档

## 🏗️ 项目结构

```
django-dev-template/
├── core/                    # Django 核心配置
│   ├── settings.py          # 项目设置
│   ├── urls.py              # 主路由配置
│   ├── wsgi.py              # WSGI 配置
│   └── asgi.py              # ASGI 配置
├── src/                     # 业务代码目录
│   ├── auth/                # 认证模块
│   │   └── auth.py          # JWT 认证实现
│   ├── user/                # 用户模块
│   │   ├── api.py           # 用户 API 路由
│   │   └── schemas.py       # Pydantic 数据模型
│   ├── router/              # API 路由聚合
│   │   └── api.py           # 主 API 入口
│   └── utils/               # 工具函数
│       ├── middleware.py    # 中间件
│       ├── jwt.py           # JWT 工具
│       ├── pagination.py    # 自定义分页
│       ├── captcha.py       # 验证码
│       └── pay.py           # 支付工具
├── apps/                    # 预留应用目录
├── templates/               # Django 模板目录
├── nginx/                   # Nginx 配置
│   └── nginx.conf           # Nginx 反向代理配置
├── .env_example             # 环境变量示例
├── .env                     # 环境变量（实际使用）
├── pyproject.toml           # 项目配置和依赖
├── uv.lock                  # uv 依赖锁定文件
├── Dockerfile               # Docker 镜像构建
└── docker-compose.yaml      # Docker Compose 配置
```

## 🚀 核心特性

### 1. Django Ninja API 框架

使用 `django-ninja` 替代传统 Django REST Framework，提供：
- 类型安全的 API 定义
- 自动生成 Swagger/OpenAPI 文档
- 高性能的异步支持
- 内置数据验证（基于 Pydantic）

### 2. JWT 认证系统

- **分层认证**: 区分普通用户 (`AuthBearer`) 和管理员 (`AdminBearer`)
- **Token 有效期**: 默认 1 小时
- **JWT 签名**: 使用 Django SECRET_KEY 进行 HS256 签名
- **自动 Token 验证**: 中间件自动处理过期和无效 Token

### 3. 统一 API 响应格式

通过 `NinjaResponseMiddleware` 中间件自动封装响应：

```json
{
  "code": 200,
  "status": "success",
  "data": { ... }
}
```

### 4. 自定义分页

支持 `skip` 和 `limit` 参数的分页查询，返回格式包含总数：

```json
{
  "items": [...],
  "total": 100,
  "limit": 20,
  "skip": 0
}
```

### 5. 可插拔功能

- **验证码**: django-simple-captcha（可通过 `CAPTCHA` 环境变量控制）
- **管理后台**: django-simpleui（可通过 `SIMPLE_UI` 环境变量控制）
- **CORS**: django-cors-headers 支持跨域请求

## 🔧 安装与运行

### 开发环境

```bash
# 克隆项目
git clone https://github.com/Rx5557770/django-dev-template.git
cd django-dev-template

# 使用 uv 创建虚拟环境并安装依赖
uv sync

# 配置环境变量
cp .env_example .env
# 编辑 .env 文件

# 运行数据库迁移
uv run python manage.py migrate

# 启动开发服务器
uv run python manage.py runserver
```

### Docker 部署

```bash
# 构建并启动容器
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

## 📚 API 文档

启动服务后访问以下地址：
- **Swagger UI**: http://localhost:8000/api/v1/docs
- **Redoc**: http://localhost:8000/api/v1/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔐 环境变量

参考 [`.env_example`](/.env_example) 配置环境变量：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEBUG` | 调试模式 | `True` |
| `SECRET_KEY` | Django 密钥 | - |
| `ALLOWED_HOSTS` | 允许的主机 | - |
| `CORS_ALLOWED_ORIGINS` | CORS 允许的源 | - |
| `SIMPLE_UI` | 是否启用 SimpleUI | `False` |
| `CAPTCHA` | 是否启用验证码 | `True` |
| `V_API_URL` | 支付 API 地址（可选） | - |
| `V_KEY` | 支付密钥（可选） | - |
| `NOTIFY_URL` | 支付回调地址（可选） | - |

## 📦 依赖包

项目主要依赖：

| 包名 | 版本 | 用途 |
|------|------|------|
| django | 5.2 | Web 框架 |
| django-ninja | >=1.6.2 | API 框架 |
| pydantic[email] | >=2.13.4 | 数据验证 |
| pyjwt | >=2.13.0 | JWT 认证 |
| django-cors-headers | >=4.9.0 | 跨域支持 |
| django-simple-captcha | >=0.6.3 | 验证码 |
| django-simpleui | >=2026.1.13 | 管理后台 |
| gunicorn | >=26.0.0 | WSGI 服务器 |
| python-decouple | >=3.8 | 环境变量管理 |
| black | >=26.5.1 | 代码格式化 |

## 🔍 核心代码分析

### 认证中间件 ([`src/auth/auth.py`](/src/auth/auth.py))

提供两种认证类：
- `AuthBearer`: 普通用户认证
- `AdminBearer`: 管理员认证（检查 `is_staff` 和 `is_active`）

### 响应中间件 ([`src/utils/middleware.py`](/src/utils/middleware.py))

`NinjaResponseMiddleware` 统一封装 API 响应，过滤掉文档路径和非 JSON 响应。

### 分页器 ([`src/utils/pagination.py`](/src/utils/pagination.py))

`CustomPagination` 实现自定义分页逻辑，默认每页 20 条，最大 20 条。

### 用户 API ([`src/user/api.py`](/src/user/api.py))

提供完整的 CRUD 操作：
- 创建用户
- 查询用户列表（支持过滤和分页）
- 查询用户详情
- 更新用户
- 删除用户

### 路由聚合 ([`src/router/api.py`](/src/router/api.py))

将各模块的 API 路由注册到主 NinjaAPI 实例，动态加载可插拔模块。

## 🌐 部署说明

### Nginx 配置

[`nginx/nginx.conf`](/nginx/nginx.conf) 配置了：
- 静态文件代理 (`/static/`)
- 媒体文件代理 (`/media/`)
- Django/Gunicorn 反向代理

**注意**: 部署前需修改 `server_name` 和文件路径。

### Docker 配置

- [`Dockerfile`](/Dockerfile): 基于 Python 3.12-slim，使用 uv 管理依赖
- [`docker-compose.yaml`](/docker-compose.yaml): 定义服务，暴露 6688 端口

启动命令执行流程：
1. 收集静态文件
2. 生成迁移文件
3. 等待并执行迁移
4. 启动 Gunicorn 服务器


### 当前架构优势

1. **现代化技术栈**: Django 5.2 + django-ninja 提供优秀的开发体验
2. **分层清晰**: 认证、业务、工具分离，职责明确
3. **可扩展性**: 预留 `apps/` 目录和可插拔模块设计
4. **生产就绪**: 包含 Docker、Nginx、Gunicorn 完整部署配置


## 📄 许可证

本项目为模板项目，可自由使用和修改。

---

**项目维护**: 欢迎提交 Issue 和 PR！
