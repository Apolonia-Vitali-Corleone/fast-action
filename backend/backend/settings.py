"""
Django 项目配置文件
包含数据库、应用、中间件等基本配置
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 密钥（生产环境需要更改）
SECRET_KEY = 'django-insecure-key-for-development-only'

# 调试模式（生产环境需要设为False）
DEBUG = True

# 允许的主机
ALLOWED_HOSTS = ['*']

# 已安装的应用
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin后台
    'django.contrib.auth',           # 认证框架
    'django.contrib.contenttypes',   # 内容类型框架
    'django.contrib.sessions',       # Session框架
    'django.contrib.messages',       # 消息框架
    'django.contrib.staticfiles',    # 静态文件管理
    'corsheaders',                   # CORS跨域支持
    'students',                      # 学生应用
    'teachers',                      # 教师应用
    'courses',                       # 课程应用
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # 安全中间件
    'corsheaders.middleware.CorsMiddleware',              # CORS中间件（必须在CommonMiddleware之前）
    'django.middleware.common.CommonMiddleware',          # 通用中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持保护
]

# URL配置
ROOT_URLCONF = 'backend.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI应用
WSGI_APPLICATION = 'backend.wsgi.application'

# 数据库配置（使用MySQL）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'course_system',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '192.168.233.136',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# 语言配置
LANGUAGE_CODE = 'zh-hans'  # 中文

# 时区配置
TIME_ZONE = 'Asia/Shanghai'  # 上海时区

USE_I18N = True  # 启用国际化
USE_TZ = True    # 启用时区支持

# 静态文件路径
STATIC_URL = 'static/'

# 默认主键类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS配置（允许前端跨域访问）
# 当使用 withCredentials 时，不能用通配符 *
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
CORS_ALLOW_CREDENTIALS = True  # 允许携带Cookie
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'POST',
    'PUT',
]
