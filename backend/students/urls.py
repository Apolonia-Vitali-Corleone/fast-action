"""
学生相关URL配置
"""
from django.urls import path
from . import views, auth_views

urlpatterns = [
    # 学生注册登录
    path('api/student/register/', views.student_register, name='student-register'),
    path('api/student/login/', views.student_login, name='student-login'),

    # 学生功能
    path('api/student/courses/', views.available_courses, name='student-courses'),
    path('api/student/my-courses/', views.my_courses, name='student-my-courses'),
    path('api/student/enroll/', views.enroll_course, name='student-enroll'),
    path('api/student/drop/', views.drop_course, name='student-drop'),

    # 通用认证
    path('api/logout/', auth_views.logout, name='logout'),
    path('api/current-user/', auth_views.current_user, name='current-user'),
]
