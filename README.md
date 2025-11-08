# Django 选课系统

一个基于 Django + Vue.js 的完整选课管理系统。

## 项目特点

- ✅ **无外键设计** - 所有关联关系在应用层处理
- ✅ **清晰的应用分离** - students、teachers、courses 独立应用
- ✅ **MySQL数据库** - 生产级数据库，提供SQL初始化脚本
- ✅ **角色分离** - 学生和教师完全独立的模型和API

## 系统角色

### 学生
- 注册/登录
- 查看可选课程
- 选课/退课
- 查看我的课程

### 教师
- 注册/登录
- 创建课程
- 删除课程
- 查看课程选课学生名单

### 管理员
- Django Admin后台管理所有数据

## 数据模型（无外键）

### students 表
```sql
id, username, password, email, created_at
```

### teachers 表
```sql
id, username, password, email, created_at
```

### courses 表
```sql
id, name, description, teacher_id (int), capacity, created_at
```

### enrollments 表
```sql
id, student_id (int), course_id (int), enrolled_at
```

**所有关联都用普通int字段，在应用层处理关联逻辑**

## API 接口

### 学生接口
- `POST /api/student/register/` - 学生注册
- `POST /api/student/login/` - 学生登录
- `GET /api/student/courses/` - 查看可选课程
- `GET /api/student/my-courses/` - 查看我的课程
- `POST /api/student/enroll/` - 选课
- `POST /api/student/drop/` - 退课

### 教师接口
- `POST /api/teacher/register/` - 教师注册
- `POST /api/teacher/login/` - 教师登录
- `GET /api/teacher/courses/` - 查看我的课程
- `POST /api/teacher/courses/create/` - 创建课程
- `DELETE /api/teacher/courses/<id>/delete/` - 删除课程
- `GET /api/teacher/courses/<id>/students/` - 查看课程学生

### 通用接口
- `POST /api/logout/` - 登出
- `GET /api/current-user/` - 获取当前用户信息

## 快速开始

### 1. 初始化MySQL数据库

```bash
# 连接MySQL
mysql -h 192.168.233.136 -u root -p

# 执行初始化脚本
source backend/init.sql
```

这将创建：
- `course_system` 数据库
- 4张表（students, teachers, courses, enrollments）
- 测试数据（2个学生，2个教师，3门课程）

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

后端运行在 `http://localhost:8000`

**注意**: 不需要运行 `makemigrations` 和 `migrate`，直接使用SQL初始化的表结构

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`

## 测试账号

### 学生账号
- 用户名: `student1` / 密码: `password123`
- 用户名: `student2` / 密码: `password123`

### 教师账号
- 用户名: `teacher1` / 密码: `password123`
- 用户名: `teacher2` / 密码: `password123`

## 项目结构

```
fast-action/
├── backend/
│   ├── students/           # 学生应用
│   │   ├── models.py       # Student模型
│   │   ├── views.py        # 学生API
│   │   ├── auth_views.py   # 通用认证
│   │   └── urls.py         # 学生路由
│   ├── teachers/           # 教师应用
│   │   ├── models.py       # Teacher模型
│   │   ├── views.py        # 教师API
│   │   └── urls.py         # 教师路由
│   ├── courses/            # 课程应用
│   │   └── models.py       # Course, Enrollment模型
│   ├── backend/
│   │   ├── settings.py     # MySQL配置
│   │   └── urls.py         # 主路由
│   ├── init.sql            # MySQL初始化脚本
│   └── requirements.txt
└── frontend/
    └── src/
        └── App.vue         # 前端主组件
```

## 技术栈

### 后端
- Django 4.2.0
- MySQL 8.0
- mysqlclient 2.2.0
- django-cors-headers 4.0.0

### 前端
- Vue 3 (Composition API)
- Axios
- Vite

## 设计理念

### 1. 无外键设计
- 数据库不使用外键约束
- 所有关联通过应用层的int字段处理
- 查询时手动join数据

### 2. 应用分离
- students、teachers、courses 独立应用
- 学生和教师不共用User模型
- 每个应用有自己的views和urls

### 3. MySQL直接初始化
- 不依赖Django migrations
- 提供SQL脚本直接创建表
- 更接近生产环境实践

## 应用层关联示例

查看课程时关联教师信息：
```python
# 获取课程
course = Course.objects.filter(id=course_id).first()

# 应用层关联：查找教师
teacher = Teacher.objects.filter(id=course.teacher_id).first()
teacher_name = teacher.username if teacher else '未知'
```

查看选课记录时关联学生和课程：
```python
# 获取选课记录
enrollment = Enrollment.objects.filter(student_id=user_id)

for e in enrollment:
    # 应用层关联：查找课程
    course = Course.objects.filter(id=e.course_id).first()

    # 应用层关联：查找教师
    teacher = Teacher.objects.filter(id=course.teacher_id).first()
```

## MySQL配置说明

在 `backend/backend/settings.py` 中：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'course_system',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '192.168.233.136',
        'PORT': '3306',
    }
}
```

## 开发说明

这是一个基础的选课系统，重点展示：
- 无外键的应用层关联设计
- 清晰的应用结构分离
- MySQL直接初始化
- 前后端分离架构

代码注重可读性和功能完整性，没有进行过度优化。
