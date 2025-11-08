# Django 选课系统

一个基于 Django + Vue.js 的完整选课管理系统，展示了 Django 的主要特性。

## 功能特性

### 用户角色
- **学生**：查看可选课程、选课、退课、管理我的课程
- **老师**：创建课程、删除课程、查看课程选课学生名单
- **管理员**：通过 Django Admin 后台管理所有数据

### Django 特性展示
- ✅ 自定义用户模型 (AbstractUser)
- ✅ 数据库关系 (ForeignKey, ManyToMany)
- ✅ 认证系统 (Session-based Authentication)
- ✅ Django Admin 后台
- ✅ RESTful API 设计
- ✅ 权限控制 (基于角色)
- ✅ 数据验证
- ✅ CORS 跨域支持

## 数据模型

### User (用户)
- 扩展 Django 的 AbstractUser
- 字段：username, email, password, role (student/teacher)

### Course (课程)
- 字段：name, description, teacher (外键), capacity, created_at
- 方法：enrolled_count(), is_full()

### Enrollment (选课记录)
- 字段：student (外键), course (外键), enrolled_at
- 约束：同一学生不能重复选同一门课 (unique_together)

### Student (旧版，保留兼容)
- 字段：name, age, major, created_at

## API 接口

### 认证相关
- `POST /api/register/` - 注册（含角色选择）
- `POST /api/login/` - 登录
- `POST /api/logout/` - 登出
- `GET /api/current-user/` - 获取当前用户信息

### 学生功能
- `GET /api/student/courses/` - 查看所有可选课程
- `GET /api/student/my-courses/` - 查看我的课程
- `POST /api/student/enroll/` - 选课
- `POST /api/student/drop/` - 退课

### 教师功能
- `GET /api/teacher/courses/` - 查看我的课程
- `POST /api/teacher/courses/create/` - 创建课程
- `DELETE /api/teacher/courses/<id>/delete/` - 删除课程
- `GET /api/teacher/courses/<id>/students/` - 查看课程选课学生

### 管理员功能
- `/admin/` - Django Admin 后台

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # 创建管理员账号
python manage.py runserver
```

后端将运行在 `http://localhost:8000`

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

前端将运行在 `http://localhost:5173`

## 使用说明

### 注册账号
1. 打开前端页面
2. 点击"注册"标签
3. 填写用户名、邮箱、密码
4. **选择身份**：学生或老师
5. 点击"注册"按钮

### 学生使用流程
1. 使用学生账号登录
2. 在"可选课程"标签查看所有课程
3. 点击"选课"按钮选择课程
4. 在"我的课程"标签查看已选课程
5. 可以点击"退课"按钮退选课程

### 教师使用流程
1. 使用教师账号登录
2. 在"创建新课程"表单中填写课程信息
3. 点击"创建课程"按钮
4. 在"我的课程"列表中查看已创建的课程
5. 点击"查看学生"查看选课学生名单
6. 可以删除不需要的课程

### 管理员使用流程
1. 访问 `http://localhost:8000/admin/`
2. 使用 superuser 账号登录
3. 管理所有用户、课程、选课记录

## 技术栈

### 后端
- Django 4.2.0
- django-cors-headers 4.0.0
- SQLite 数据库

### 前端
- Vue 3 (Composition API)
- Axios (HTTP 客户端)
- Vite (构建工具)

## 项目结构

```
fast-action/
├── backend/
│   ├── backend/
│   │   ├── settings.py      # Django 配置
│   │   ├── urls.py          # 主路由
│   │   └── wsgi.py
│   ├── students/
│   │   ├── models.py        # 数据模型
│   │   ├── views.py         # API 视图
│   │   ├── urls.py          # API 路由
│   │   └── admin.py         # Admin 配置
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue          # 主组件
│   │   └── main.js          # 入口文件
│   ├── index.html
│   └── package.json
└── README.md
```

## 注意事项

- 本项目使用 Session 认证，需要配置 CORS 支持跨域 Cookie
- 为了简化，CSRF 验证在部分接口中被禁用（生产环境需启用）
- 数据库使用 SQLite，生产环境建议使用 PostgreSQL 或 MySQL
- Admin 后台可以管理所有数据，包括用户、课程、选课记录

## Django 特性说明

### 1. 自定义用户模型
通过继承 `AbstractUser` 扩展用户模型，添加 `role` 字段区分学生和老师。

### 2. 模型关系
- `Course.teacher` → `User` (多对一)
- `Enrollment.student` → `User` (多对一)
- `Enrollment.course` → `Course` (多对一)
- 实现了学生和课程的多对多关系

### 3. 认证与权限
- 使用 Django 自带的认证系统
- 基于 Session 的认证机制
- 在视图中检查用户角色实现权限控制

### 4. Django Admin
- 注册所有模型到 Admin
- 自定义显示字段和过滤器
- 支持搜索和排序

### 5. 数据验证
- 模型层约束：unique_together, ForeignKey
- 视图层验证：检查课程容量、重复选课

## 开发说明

这是一个基础的选课系统，重点在于展示 Django 的核心特性：
- 完整的用户认证流程
- 数据库关系设计
- RESTful API 设计
- 前后端分离架构

代码注重可读性和功能完整性，没有进行过度优化。
