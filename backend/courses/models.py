"""
课程和选课数据模型
"""
from django.db import models


class Course(models.Model):
    """课程模型 - 不用外键，用teacher_id"""
    name = models.CharField(max_length=200, verbose_name='课程名称')
    description = models.TextField(blank=True, verbose_name='课程描述')
    teacher_id = models.IntegerField(verbose_name='教师ID')  # 普通int，不用外键
    capacity = models.IntegerField(default=50, verbose_name='容量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'courses'
        verbose_name = '课程'
        verbose_name_plural = '课程'

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """选课记录模型 - 不用外键"""
    student_id = models.IntegerField(verbose_name='学生ID')  # 普通int
    course_id = models.IntegerField(verbose_name='课程ID')   # 普通int
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='选课时间')

    class Meta:
        db_table = 'enrollments'
        verbose_name = '选课记录'
        verbose_name_plural = '选课记录'
        # 应用层保证唯一性，不在数据库层
        indexes = [
            models.Index(fields=['student_id', 'course_id']),
        ]

    def __str__(self):
        return f'Student {self.student_id} - Course {self.course_id}'
