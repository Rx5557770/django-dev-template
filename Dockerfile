FROM python:3.12-slim

# 容器的工作目录
WORKDIR /app

# 关闭 Python 输出缓冲，日志实时打印
ENV PYTHONUNBUFFERED=1
# 不生成 .pyc 文件，减小镜像体积
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y netcat-openbsd default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# 安装uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

# 安装项目依赖
RUN uv sync

# 声明对外暴露端口
EXPOSE 6688

# 执行命令
CMD ["uv run gunicorn core.wsgi:application --bind 0.0.0.0:6688"]
