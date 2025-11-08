#!/usr/bin/env python
"""
Django 项目管理脚本
用于启动服务器、数据库迁移等操作
"""
import os
import sys

if __name__ == '__main__':
    # 设置Django配置文件路径
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。请确保已安装Django。"
        ) from exc
    # 执行命令行命令
    execute_from_command_line(sys.argv)
