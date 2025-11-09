"""
学生数据模型
"""
from django.db import models
import bcrypt


class Student(models.Model):
    """学生模型"""
    username = models.CharField(max_length=100, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'students'
        verbose_name = '学生'
        verbose_name_plural = '学生'

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """设置密码"""
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self, raw_password):
        """验证密码"""
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))
