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

    # 选课系统API路由
    path('', include('students.urls')),
]
