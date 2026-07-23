from decouple import config

if config("CELERY", cast=bool, default=False):
    import os
    from datetime import timedelta

    from celery import Celery, shared_task
    from django.core.management import call_command

    # 设置 Django 默认配置模块
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    app = Celery("core")

    # 读取 settings.py 中所有 CELERY_ 开头的配置项
    app.config_from_object("django.conf:settings", namespace="CELERY")

    # 自动去各个已注册的 App 下寻找 tasks.py 文件
    app.autodiscover_tasks()

    # app.conf.imports = ("src.utils.tasks",) # 非Django app 需要手动注册

    @shared_task
    def backup():
        call_command(
            "dbbackup", clean=True, compress=True
        )  # 清理旧备份,并以压缩形式备份数据

    #  定时任务
    app.conf.beat_schedule = {
        "backup": {
            "task": "core.celery.backup",  # 运行路径
            "schedule": timedelta(minutes=15),  # 规则
        }
    }
