"""
教师相关API
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Teacher
from courses.models import Course, Enrollment
from students.models import Student


# ==================== 认证相关 ====================

@csrf_exempt
@require_http_methods(["POST"])
def teacher_register(request):
    """教师注册"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not all([username, password, email]):
            return JsonResponse({'error': '所有字段都是必填的'}, status=400)

        # 检查用户名是否已存在
        if Teacher.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=400)

        if Teacher.objects.filter(email=email).exists():
            return JsonResponse({'error': '邮箱已存在'}, status=400)

        # 创建教师
        teacher = Teacher(username=username, email=email)
        teacher.set_password(password)
        teacher.save()

        return JsonResponse({
            'message': '注册成功',
            'user': {
                'id': teacher.id,
                'username': teacher.username,
                'email': teacher.email,
                'role': 'teacher'
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def teacher_login(request):
    """教师登录"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        teacher = Teacher.objects.filter(username=username).first()

        if teacher and teacher.check_password(password):
            # 保存session
            request.session['user_id'] = teacher.id
            request.session['user_role'] = 'teacher'

            return JsonResponse({
                'message': '登录成功',
                'user': {
                    'id': teacher.id,
                    'username': teacher.username,
                    'email': teacher.email,
                    'role': 'teacher'
                }
            })
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== 教师功能 ====================

@require_http_methods(["GET"])
def my_courses(request):
    """查看我的课程"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'teacher':
        return JsonResponse({'error': '请先登录'}, status=401)

    # 应用层关联：查找该教师的所有课程
    courses = Course.objects.filter(teacher_id=user_id)

    data = []
    for c in courses:
        # 计算已选人数
        enrolled_count = Enrollment.objects.filter(course_id=c.id).count()

        data.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'capacity': c.capacity,
            'enrolled': enrolled_count,
            'is_full': enrolled_count >= c.capacity,
            'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'courses': data})


@csrf_exempt
@require_http_methods(["POST"])
def create_course(request):
    """创建课程"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'teacher':
        return JsonResponse({'error': '请先登录'}, status=401)

    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        capacity = data.get('capacity', 50)

        if not name:
            return JsonResponse({'error': '课程名称不能为空'}, status=400)

        # 创建课程，teacher_id是普通int字段
        course = Course.objects.create(
            name=name,
            description=description,
            teacher_id=user_id,  # 应用层关联
            capacity=capacity
        )

        return JsonResponse({
            'message': '课程创建成功',
            'course': {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'capacity': course.capacity
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_course(request, course_id):
    """删除课程"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'teacher':
        return JsonResponse({'error': '请先登录'}, status=401)

    try:
        # 应用层验证：检查课程是否属于该教师
        course = Course.objects.filter(id=course_id, teacher_id=user_id).first()

        if not course:
            return JsonResponse({'error': '课程不存在或您不是该课程的教师'}, status=404)

        course_name = course.name

        # 删除相关选课记录
        Enrollment.objects.filter(course_id=course_id).delete()

        # 删除课程
        course.delete()

        return JsonResponse({
            'message': f'已删除课程：{course_name}'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def course_students(request, course_id):
    """查看课程的选课学生"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'teacher':
        return JsonResponse({'error': '请先登录'}, status=401)

    try:
        # 应用层验证：检查课程是否属于该教师
        course = Course.objects.filter(id=course_id, teacher_id=user_id).first()

        if not course:
            return JsonResponse({'error': '课程不存在或您不是该课程的教师'}, status=404)

        # 获取选课记录
        enrollments = Enrollment.objects.filter(course_id=course_id)

        students = []
        for e in enrollments:
            # 应用层关联：查找学生信息
            student = Student.objects.filter(id=e.student_id).first()
            if student:
                students.append({
                    'id': student.id,
                    'username': student.username,
                    'email': student.email,
                    'enrolled_at': e.enrolled_at.strftime('%Y-%m-%d %H:%M:%S')
                })

        return JsonResponse({
            'course': {
                'id': course.id,
                'name': course.name
            },
            'students': students,
            'total': len(students)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
