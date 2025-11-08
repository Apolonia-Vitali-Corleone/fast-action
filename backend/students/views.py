"""
学生相关API
"""
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
from courses.models import Course, Enrollment
from teachers.models import Teacher


# ==================== 认证相关 ====================

@csrf_exempt
@require_http_methods(["POST"])
def student_register(request):
    """学生注册"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not all([username, password, email]):
            return JsonResponse({'error': '所有字段都是必填的'}, status=400)

        # 检查用户名是否已存在
        if Student.objects.filter(username=username).exists():
            return JsonResponse({'error': '用户名已存在'}, status=400)

        if Student.objects.filter(email=email).exists():
            return JsonResponse({'error': '邮箱已存在'}, status=400)

        # 创建学生
        student = Student(username=username, email=email)
        student.set_password(password)
        student.save()

        return JsonResponse({
            'message': '注册成功',
            'user': {
                'id': student.id,
                'username': student.username,
                'email': student.email,
                'role': 'student'
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def student_login(request):
    """学生登录"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        student = Student.objects.filter(username=username).first()

        if student and student.check_password(password):
            # 保存session
            request.session['user_id'] = student.id
            request.session['user_role'] = 'student'

            return JsonResponse({
                'message': '登录成功',
                'user': {
                    'id': student.id,
                    'username': student.username,
                    'email': student.email,
                    'role': 'student'
                }
            })
        else:
            return JsonResponse({'error': '用户名或密码错误'}, status=401)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== 学生功能 ====================

@require_http_methods(["GET"])
def available_courses(request):
    """查看可选课程"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'student':
        return JsonResponse({'error': '请先登录'}, status=401)

    # 获取所有课程
    courses = Course.objects.all()

    # 获取该学生已选课程ID列表
    enrolled_ids = list(Enrollment.objects.filter(
        student_id=user_id
    ).values_list('course_id', flat=True))

    data = []
    for c in courses:
        # 应用层关联：查找教师信息
        teacher = Teacher.objects.filter(id=c.teacher_id).first()
        teacher_name = teacher.username if teacher else '未知'

        # 计算已选人数
        enrolled_count = Enrollment.objects.filter(course_id=c.id).count()

        data.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'teacher': teacher_name,
            'capacity': c.capacity,
            'enrolled': enrolled_count,
            'is_full': enrolled_count >= c.capacity,
            'is_enrolled': c.id in enrolled_ids
        })

    return JsonResponse({'courses': data})


@require_http_methods(["GET"])
def my_courses(request):
    """查看我的课程"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'student':
        return JsonResponse({'error': '请先登录'}, status=401)

    # 获取选课记录
    enrollments = Enrollment.objects.filter(student_id=user_id)

    data = []
    for e in enrollments:
        # 应用层关联：查找课程信息
        course = Course.objects.filter(id=e.course_id).first()
        if not course:
            continue

        # 应用层关联：查找教师信息
        teacher = Teacher.objects.filter(id=course.teacher_id).first()
        teacher_name = teacher.username if teacher else '未知'

        data.append({
            'enrollment_id': e.id,
            'course_id': course.id,
            'course_name': course.name,
            'description': course.description,
            'teacher': teacher_name,
            'enrolled_at': e.enrolled_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'courses': data})


@csrf_exempt
@require_http_methods(["POST"])
def enroll_course(request):
    """选课"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'student':
        return JsonResponse({'error': '请先登录'}, status=401)

    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')

        # 检查课程是否存在
        course = Course.objects.filter(id=course_id).first()
        if not course:
            return JsonResponse({'error': '课程不存在'}, status=404)

        # 检查是否已选过
        if Enrollment.objects.filter(student_id=user_id, course_id=course_id).exists():
            return JsonResponse({'error': '您已经选过这门课了'}, status=400)

        # 检查是否已满
        enrolled_count = Enrollment.objects.filter(course_id=course_id).count()
        if enrolled_count >= course.capacity:
            return JsonResponse({'error': '课程已满'}, status=400)

        # 创建选课记录
        enrollment = Enrollment.objects.create(
            student_id=user_id,
            course_id=course_id
        )

        return JsonResponse({
            'message': '选课成功',
            'enrollment': {
                'id': enrollment.id,
                'course_name': course.name,
                'enrolled_at': enrollment.enrolled_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def drop_course(request):
    """退课"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or user_role != 'student':
        return JsonResponse({'error': '请先登录'}, status=401)

    try:
        data = json.loads(request.body)
        course_id = data.get('course_id')

        # 查找选课记录
        enrollment = Enrollment.objects.filter(
            student_id=user_id,
            course_id=course_id
        ).first()

        if not enrollment:
            return JsonResponse({'error': '未找到选课记录'}, status=404)

        # 删除选课记录
        course = Course.objects.filter(id=course_id).first()
        course_name = course.name if course else '未知课程'
        enrollment.delete()

        return JsonResponse({
            'message': f'已退选课程：{course_name}'
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
