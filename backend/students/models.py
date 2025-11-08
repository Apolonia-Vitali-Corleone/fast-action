"""
数据模型
定义选课系统的所有数据库表结构
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户模型
    扩展Django自带的User，添加角色字段
    """
    ROLE_CHOICES = [
        ('student', '学生'),
        ('teacher', '老师'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    email = models.EmailField(unique=True, verbose_name='邮箱')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'


class Course(models.Model):
    """
    课程模型
    存储课程信息
    """
    name = models.CharField(max_length=200, verbose_name='课程名称')
    description = models.TextField(blank=True, verbose_name='课程描述')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name='授课教师')
    capacity = models.IntegerField(default=50, verbose_name='容量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = '课程'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.teacher.username}'

    def enrolled_count(self):
        """已选课人数"""
        return self.enrollments.count()

    def is_full(self):
        """是否已满"""
        return self.enrolled_count() >= self.capacity


class Enrollment(models.Model):
    """
    选课记录模型
    学生和课程的多对多关系
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程')
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='选课时间')

    class Meta:
        db_table = 'enrollments'
        verbose_name = '选课记录'
        verbose_name_plural = '选课记录'
        unique_together = ['student', 'course']  # 同一学生不能重复选同一门课
        ordering = ['-enrolled_at']

    def __str__(self):
        return f'{self.student.username} - {self.course.name}'


# 保留原Student模型用于向后兼容
class Student(models.Model):
    """
    学生模型类（废弃，保留用于兼容）
    """
    name = models.CharField(max_length=100, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    major = models.CharField(max_length=200, verbose_name='专业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'students'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name} - {self.major}'
