"""
WSGI配置文件
用于部署Django应用
"""
import os
from django.core.wsgi import get_wsgi_application

# 设置Django配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 获取WSGI应用
application = get_wsgi_application()
