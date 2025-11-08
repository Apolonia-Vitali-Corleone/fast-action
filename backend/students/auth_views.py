"""
通用认证接口
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
from teachers.models import Teacher


@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    """登出"""
    request.session.flush()
    return JsonResponse({'message': '登出成功'})


@require_http_methods(["GET"])
def current_user(request):
    """获取当前登录用户信息"""
    user_id = request.session.get('user_id')
    user_role = request.session.get('user_role')

    if not user_id or not user_role:
        return JsonResponse({'error': '未登录'}, status=401)

    # 根据角色查找用户
    if user_role == 'student':
        user = Student.objects.filter(id=user_id).first()
    elif user_role == 'teacher':
        user = Teacher.objects.filter(id=user_id).first()
    else:
        return JsonResponse({'error': '无效的角色'}, status=400)

    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    return JsonResponse({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user_role
        }
    })
