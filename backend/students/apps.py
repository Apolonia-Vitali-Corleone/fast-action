"""
学生应用配置
"""
from django.apps import AppConfig


class StudentsConfig(AppConfig):
    """学生应用配置类"""
    # 默认自动字段类型
    default_auto_field = 'django.db.models.BigAutoField'
    # 应用名称
    name = 'students'
    # 应用的中文名称
    verbose_name = '学生管理'
