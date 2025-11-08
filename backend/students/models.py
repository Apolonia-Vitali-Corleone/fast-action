"""
学生数据模型
定义学生信息的数据库表结构
"""
from django.db import models

class Student(models.Model):
    """
    学生模型类
    包含学生的基本信息：姓名、年龄、专业
    """
    # 学生姓名，最大长度100字符
    name = models.CharField(max_length=100, verbose_name='姓名')

    # 学生年龄，整数类型
    age = models.IntegerField(verbose_name='年龄')

    # 学生专业，最大长度200字符
    major = models.CharField(max_length=200, verbose_name='专业')

    # 创建时间，自动记录
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        # 数据库表名
        db_table = 'students'
        # 排序方式：按ID降序
        ordering = ['-id']

    def __str__(self):
        """字符串表示"""
        return f'{self.name} - {self.major}'
