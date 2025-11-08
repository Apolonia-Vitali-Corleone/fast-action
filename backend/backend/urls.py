"""
Django URL配置
定义所有的URL路由
"""
from django.contrib import admin
from django.urls import path, include

# URL路由配置
urlpatterns = [
    # Django Admin后台
    path('admin/', admin.site.urls),

    # 学生相关API
    path('', include('students.urls')),

    # 教师相关API
    path('', include('teachers.urls')),
]
