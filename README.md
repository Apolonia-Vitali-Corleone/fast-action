# 学生信息管理系统

一个简单的学生信息增删改查系统，前端使用Vue3，后端使用Django，数据库使用SQLite。

## 项目结构

```
fast-action/
├── backend/                # Django后端
│   ├── backend/           # Django配置
│   │   ├── __init__.py
│   │   ├── settings.py    # 项目配置
│   │   ├── urls.py        # URL路由
│   │   └── wsgi.py        # WSGI配置
│   ├── students/          # 学生应用
│   │   ├── __init__.py
│   │   ├── apps.py        # 应用配置
│   │   ├── models.py      # 数据模型
│   │   ├── views.py       # 视图函数
│   │   └── urls.py        # 应用路由
│   ├── manage.py          # Django管理脚本
│   └── requirements.txt   # Python依赖
├── frontend/              # Vue3前端
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   └── main.js        # 入口文件
│   ├── index.html         # HTML模板
│   ├── package.json       # npm配置
│   └── vite.config.js     # Vite配置
└── README.md              # 项目说明
```

## 功能特性

- 查看所有学生信息
- 添加新学生
- 编辑学生信息
- 删除学生

## 技术栈

### 后端
- Django 4.2.0
- SQLite数据库
- django-cors-headers（跨域支持）

### 前端
- Vue 3.3.4
- Vite 4.4.0
- Axios（HTTP请求）

## 安装运行

### 后端启动

1. 进入后端目录
```bash
cd backend
```

2. 安装Python依赖
```bash
pip install -r requirements.txt
```

3. 执行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

4. 启动Django服务器
```bash
python manage.py runserver
```

后端将运行在 http://localhost:8000

### 前端启动

1. 进入前端目录
```bash
cd frontend
```

2. 安装npm依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

前端将运行在 http://localhost:5173

## API接口

### 获取所有学生
```
GET http://localhost:8000/api/students/
```

### 创建学生
```
POST http://localhost:8000/api/students/
Content-Type: application/json

{
  "name": "张三",
  "age": 20,
  "major": "计算机科学"
}
```

### 获取单个学生
```
GET http://localhost:8000/api/students/{id}/
```

### 更新学生
```
PUT http://localhost:8000/api/students/{id}/
Content-Type: application/json

{
  "name": "李四",
  "age": 21,
  "major": "软件工程"
}
```

### 删除学生
```
DELETE http://localhost:8000/api/students/{id}/
```

## 注意事项

1. 这是一个最基础的示例项目，仅用于学习和演示
2. 没有进行任何安全性和健壮性优化
3. 生产环境需要修改SECRET_KEY和数据库配置
4. CORS配置允许所有来源，生产环境需要限制
5. 没有用户认证和权限控制
6. 没有数据验证和错误处理优化

## 开发说明

- 所有代码都有详细的中文注释
- 采用最简单的实现方式
- 不考虑性能优化和复杂场景
- 适合初学者学习前后端分离开发

## 许可证

MIT
