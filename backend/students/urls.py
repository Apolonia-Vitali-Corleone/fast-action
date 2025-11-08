"""
选课系统URL配置
定义所有API路由
"""
from django.urls import path
from . import views

urlpatterns = [
    # ========== 认证相关 ==========
    path('api/register/', views.register, name='register'),
    path('api/login/', views.user_login, name='login'),
    path('api/logout/', views.user_logout, name='logout'),
    path('api/current-user/', views.current_user, name='current-user'),

    # ========== 学生相关 ==========
    path('api/student/courses/', views.student_courses, name='student-courses'),
    path('api/student/my-courses/', views.my_courses, name='my-courses'),
    path('api/student/enroll/', views.enroll_course, name='enroll-course'),
    path('api/student/drop/', views.drop_course, name='drop-course'),

    # ========== 教师相关 ==========
    path('api/teacher/courses/', views.teacher_courses, name='teacher-courses'),
    path('api/teacher/courses/create/', views.create_course, name='create-course'),
    path('api/teacher/courses/<int:course_id>/delete/', views.delete_course, name='delete-course'),
    path('api/teacher/courses/<int:course_id>/students/', views.course_students, name='course-students'),

    # ========== 旧接口（兼容） ==========
    path('api/students/', views.student_list, name='student-list'),
    path('api/students/<int:pk>/', views.student_detail, name='student-detail'),
]
