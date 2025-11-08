"""
学生信息视图
处理学生信息的增删改查请求
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student


@csrf_exempt  # 禁用CSRF验证（生产环境不推荐）
@require_http_methods(["GET", "POST"])  # 只允许GET和POST请求
def student_list(request):
    """
    学生列表接口
    GET: 获取所有学生
    POST: 创建新学生
    """
    if request.method == 'GET':
        # 查询所有学生
        students = Student.objects.all()
        # 转换为字典列表
        data = [{
            'id': s.id,
            'name': s.name,
            'age': s.age,
            'major': s.major
        } for s in students]
        # 返回JSON响应
        return JsonResponse({'students': data})

    elif request.method == 'POST':
        # 解析请求体中的JSON数据
        data = json.loads(request.body)
        # 创建新学生
        student = Student.objects.create(
            name=data['name'],
            age=data['age'],
            major=data['major']
        )
        # 返回创建的学生信息
        return JsonResponse({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })


@csrf_exempt  # 禁用CSRF验证
@require_http_methods(["GET", "PUT", "DELETE"])  # 允许GET、PUT、DELETE请求
def student_detail(request, pk):
    """
    学生详情接口
    GET: 获取指定学生
    PUT: 更新指定学生
    DELETE: 删除指定学生
    """
    try:
        # 根据ID查询学生
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        # 学生不存在，返回404错误
        return JsonResponse({'error': '学生不存在'}, status=404)

    if request.method == 'GET':
        # 返回学生信息
        return JsonResponse({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })

    elif request.method == 'PUT':
        # 解析请求体中的JSON数据
        data = json.loads(request.body)
        # 更新学生信息
        student.name = data.get('name', student.name)
        student.age = data.get('age', student.age)
        student.major = data.get('major', student.major)
        student.save()  # 保存到数据库
        # 返回更新后的学生信息
        return JsonResponse({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })

    elif request.method == 'DELETE':
        # 删除学生
        student.delete()
        # 返回成功消息
        return JsonResponse({'message': '删除成功'})
