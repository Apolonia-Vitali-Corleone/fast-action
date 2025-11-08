"""
学生应用URL配置
定义学生相关的API路由
"""
from django.urls import path
from . import views

# URL路由配置
urlpatterns = [
    # 学生列表：GET获取所有学生，POST创建新学生
    path('', views.student_list, name='student-list'),

    # 学生详情：GET获取单个学生，PUT更新学生，DELETE删除学生
    path('<int:pk>/', views.student_detail, name='student-detail'),
]
