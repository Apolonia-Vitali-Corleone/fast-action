"""
Django URL配置
定义所有的URL路由
"""
from django.urls import path, include

# URL路由配置
urlpatterns = [
    # 学生信息相关路由，前缀为 /api/students/
    path('api/students/', include('students.urls')),
]
