"""
选课系统视图
处理认证和业务逻辑
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import User, Course, Enrollment, Student


# ==================== 认证相关接口 ====================

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """
    注册接口
    POST: 创建新用户（学生或老师）
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role')  # 'student' or 'teacher'

        # 验证必填字段
        if not all([username, password, email, role]):
            return JsonResponse({'error': '所有字段都是必填的'}, status=400)

        if role not in ['student', 'teacher']:
            return JsonResponse({'error': '角色必须是student或teacher'}, status=400)

        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=role
        )

        return JsonResponse({
            'message': '注册成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }, status=201)

    except IntegrityError:
        return JsonResponse({'error': '用户名或邮箱已存在'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    """
    登录接口
    POST: 验证用户并创建session
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': '登录成功',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            })
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def user_logout(request):
    """
    登出接口
    POST: 销毁session
    """
    logout(request)
    return JsonResponse({'message': '登出成功'})


@require_http_methods(["GET"])
def current_user(request):
    """
    获取当前登录用户信息
    GET: 返回当前用户
    """
    if request.user.is_authenticated:
        return JsonResponse({
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'role': request.user.role
            }
        })
    else:
        return JsonResponse({'error': '未登录'}, status=401)


# ==================== 学生相关接口 ====================

@require_http_methods(["GET"])
def student_courses(request):
    """
    学生查看可选课程
    GET: 返回所有课程列表
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'student':
        return JsonResponse({'error': '只有学生可以访问'}, status=403)

    # 获取所有课程
    courses = Course.objects.all()

    # 获取学生已选课程ID列表
    enrolled_ids = Enrollment.objects.filter(
        student=request.user
    ).values_list('course_id', flat=True)

    data = [{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'teacher': c.teacher.username,
        'capacity': c.capacity,
        'enrolled': c.enrolled_count(),
        'is_full': c.is_full(),
        'is_enrolled': c.id in enrolled_ids
    } for c in courses]

    return JsonResponse({'courses': data})


@require_http_methods(["GET"])
def my_courses(request):
    """
    学生查看我的课程
    GET: 返回已选课程列表
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'student':
        return JsonResponse({'error': '只有学生可以访问'}, status=403)

    enrollments = Enrollment.objects.filter(student=request.user).select_related('course', 'course__teacher')

    data = [{
        'enrollment_id': e.id,
        'course_id': e.course.id,
        'course_name': e.course.name,
        'description': e.course.description,
        'teacher': e.course.teacher.username,
        'enrolled_at': e.enrolled_at.strftime('%Y-%m-%d %H:%M:%S')
    } for e in enrollments]

    return JsonResponse({'courses': data})


@csrf_exempt
@require_http_methods(["POST"])
def enroll_course(request):
    """
    学生选课
    POST: 选择一门课程
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'student':
        return JsonResponse({'error': '只有学生可以选课'}, status=403)

    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')

        # 获取课程
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({'error': '课程不存在'}, status=404)

        # 检查是否已满
        if course.is_full():
            return JsonResponse({'error': '课程已满'}, status=400)

        # 创建选课记录
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course
        )

        return JsonResponse({
            'message': '选课成功',
            'enrollment': {
                'id': enrollment.id,
                'course_name': course.name,
                'enrolled_at': enrollment.enrolled_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)

    except IntegrityError:
        return JsonResponse({'error': '您已经选过这门课了'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def drop_course(request):
    """
    学生退课
    POST: 退选一门课程
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'student':
        return JsonResponse({'error': '只有学生可以退课'}, status=403)

    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')

        # 查找选课记录
        try:
            enrollment = Enrollment.objects.get(
                student=request.user,
                course_id=course_id
            )
        except Enrollment.DoesNotExist:
            return JsonResponse({'error': '未找到选课记录'}, status=404)

        # 删除选课记录
        course_name = enrollment.course.name
        enrollment.delete()

        return JsonResponse({
            'message': f'已退选课程：{course_name}'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== 教师相关接口 ====================

@require_http_methods(["GET"])
def teacher_courses(request):
    """
    教师查看我的课程
    GET: 返回教师创建的所有课程
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'teacher':
        return JsonResponse({'error': '只有教师可以访问'}, status=403)

    courses = Course.objects.filter(teacher=request.user)

    data = [{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'capacity': c.capacity,
        'enrolled': c.enrolled_count(),
        'is_full': c.is_full(),
        'created_at': c.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for c in courses]

    return JsonResponse({'courses': data})


@csrf_exempt
@require_http_methods(["POST"])
def create_course(request):
    """
    教师创建课程
    POST: 创建一门新课程
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'teacher':
        return JsonResponse({'error': '只有教师可以创建课程'}, status=403)

    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        capacity = data.get('capacity', 50)

        if not name:
            return JsonResponse({'error': '课程名称不能为空'}, status=400)

        course = Course.objects.create(
            name=name,
            description=description,
            teacher=request.user,
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
    """
    教师删除课程
    DELETE: 删除一门课程
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'teacher':
        return JsonResponse({'error': '只有教师可以删除课程'}, status=403)

    try:
        course = Course.objects.get(id=course_id, teacher=request.user)
        course_name = course.name
        course.delete()

        return JsonResponse({
            'message': f'已删除课程：{course_name}'
        })

    except Course.DoesNotExist:
        return JsonResponse({'error': '课程不存在或您不是该课程的教师'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def course_students(request, course_id):
    """
    教师查看课程的选课学生
    GET: 返回选课学生列表
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '请先登录'}, status=401)

    if request.user.role != 'teacher':
        return JsonResponse({'error': '只有教师可以查看'}, status=403)

    try:
        # 验证是否是该课程的教师
        course = Course.objects.get(id=course_id, teacher=request.user)

        # 获取选课学生
        enrollments = Enrollment.objects.filter(course=course).select_related('student')

        students = [{
            'id': e.student.id,
            'username': e.student.username,
            'email': e.student.email,
            'enrolled_at': e.enrolled_at.strftime('%Y-%m-%d %H:%M:%S')
        } for e in enrollments]

        return JsonResponse({
            'course': {
                'id': course.id,
                'name': course.name
            },
            'students': students,
            'total': len(students)
        })

    except Course.DoesNotExist:
        return JsonResponse({'error': '课程不存在或您不是该课程的教师'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== 旧的Student接口（保留兼容） ====================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def student_list(request):
    """
    学生列表接口（旧版，保留兼容）
    """
    if request.method == 'GET':
        students = Student.objects.all()
        data = [{
            'id': s.id,
            'name': s.name,
            'age': s.age,
            'major': s.major
        } for s in students]
        return JsonResponse({'students': data})

    elif request.method == 'POST':
        data = json.loads(request.body)
        student = Student.objects.create(
            name=data['name'],
            age=data['age'],
            major=data['major']
        )
        return JsonResponse({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def student_detail(request, pk):
    """
    学生详情接口（旧版，保留兼容）
    """
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return JsonResponse({'error': '学生不存在'}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })

    elif request.method == 'PUT':
        data = json.loads(request.body)
        student.name = data.get('name', student.name)
        student.age = data.get('age', student.age)
        student.major = data.get('major', student.major)
        student.save()
        return JsonResponse({
            'id': student.id,
            'name': student.name,
            'age': student.age,
            'major': student.major
        })

    elif request.method == 'DELETE':
        student.delete()
        return JsonResponse({'message': '删除成功'})
