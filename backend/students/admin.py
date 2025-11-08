"""
Django Admin后台配置
管理员可以管理所有数据
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course, Enrollment, Student


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('额外信息', {'fields': ('role',)}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """课程管理"""
    list_display = ['name', 'teacher', 'capacity', 'get_enrolled_count', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'teacher__username']
    ordering = ['-created_at']

    def get_enrolled_count(self, obj):
        """显示已选人数"""
        return obj.enrolled_count()
    get_enrolled_count.short_description = '已选人数'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """选课记录管理"""
    list_display = ['student', 'course', 'enrolled_at']
    list_filter = ['enrolled_at', 'course']
    search_fields = ['student__username', 'course__name']
    ordering = ['-enrolled_at']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """学生信息管理（旧版）"""
    list_display = ['name', 'age', 'major', 'created_at']
    list_filter = ['major', 'created_at']
    search_fields = ['name', 'major']
    ordering = ['-created_at']
