"""
教师数据模型
"""
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Teacher(models.Model):
    """教师模型"""
    username = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'teachers'
        verbose_name = '教师'
        verbose_name_plural = '教师'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """设置密码"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password)
