"""
教师相关URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    # 教师注册登录
    path('api/teacher/register/', views.teacher_register, name='teacher-register'),
    path('api/teacher/login/', views.teacher_login, name='teacher-login'),

    # 教师功能
    path('api/teacher/courses/', views.my_courses, name='teacher-courses'),
    path('api/teacher/courses/create/', views.create_course, name='teacher-create-course'),
    path('api/teacher/courses/<int:course_id>/delete/', views.delete_course, name='teacher-delete-course'),
    path('api/teacher/courses/<int:course_id>/students/', views.course_students, name='teacher-course-students'),
]
