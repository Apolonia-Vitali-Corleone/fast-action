<template>
  <!-- 主容器 -->
  <div class="container">
    <!-- 页面标题 -->
    <h1>学生信息管理系统</h1>

    <!-- 添加学生表单 -->
    <div class="form-box">
      <h2>{{ editingId ? '编辑学生' : '添加学生' }}</h2>
      <form @submit.prevent="saveStudent">
        <!-- 姓名输入框 -->
        <div class="form-group">
          <label>姓名：</label>
          <input v-model="form.name" type="text" required placeholder="请输入姓名">
        </div>

        <!-- 年龄输入框 -->
        <div class="form-group">
          <label>年龄：</label>
          <input v-model="form.age" type="number" required placeholder="请输入年龄">
        </div>

        <!-- 专业输入框 -->
        <div class="form-group">
          <label>专业：</label>
          <input v-model="form.major" type="text" required placeholder="请输入专业">
        </div>

        <!-- 提交按钮 -->
        <div class="form-buttons">
          <button type="submit" class="btn btn-primary">
            {{ editingId ? '更新' : '添加' }}
          </button>
          <!-- 取消编辑按钮 -->
          <button v-if="editingId" type="button" @click="cancelEdit" class="btn btn-secondary">
            取消
          </button>
        </div>
      </form>
    </div>

    <!-- 学生列表 -->
    <div class="table-box">
      <h2>学生列表</h2>
      <!-- 没有学生时显示提示 -->
      <p v-if="students.length === 0" class="empty-text">暂无学生信息</p>
      <!-- 学生信息表格 -->
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th>姓名</th>
            <th>年龄</th>
            <th>专业</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <!-- 循环渲染每个学生 -->
          <tr v-for="student in students" :key="student.id">
            <td>{{ student.id }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.age }}</td>
            <td>{{ student.major }}</td>
            <td>
              <!-- 编辑按钮 -->
              <button @click="editStudent(student)" class="btn btn-edit">编辑</button>
              <!-- 删除按钮 -->
              <button @click="deleteStudent(student.id)" class="btn btn-delete">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
/**
 * Vue3组合式API
 * 使用ref和reactive管理组件状态
 */
import { ref, onMounted } from 'vue'
import axios from 'axios'

// 后端API地址
const API_URL = 'http://localhost:8000/api/students/'

// 学生列表数据
const students = ref([])

// 表单数据
const form = ref({
  name: '',
  age: '',
  major: ''
})

// 正在编辑的学生ID（null表示添加模式）
const editingId = ref(null)

/**
 * 获取所有学生列表
 */
const fetchStudents = async () => {
  try {
    // 发送GET请求获取学生列表
    const response = await axios.get(API_URL)
    // 更新学生列表
    students.value = response.data.students
  } catch (error) {
    console.error('获取学生列表失败:', error)
    alert('获取学生列表失败')
  }
}

/**
 * 保存学生（新增或更新）
 */
const saveStudent = async () => {
  try {
    if (editingId.value) {
      // 更新模式：发送PUT请求
      await axios.put(`${API_URL}${editingId.value}/`, form.value)
      alert('更新成功')
    } else {
      // 添加模式：发送POST请求
      await axios.post(API_URL, form.value)
      alert('添加成功')
    }
    // 重新获取学生列表
    await fetchStudents()
    // 重置表单
    resetForm()
  } catch (error) {
    console.error('保存失败:', error)
    alert('保存失败')
  }
}

/**
 * 编辑学生
 * 将学生信息填充到表单中
 */
const editStudent = (student) => {
  // 设置编辑ID
  editingId.value = student.id
  // 填充表单数据
  form.value = {
    name: student.name,
    age: student.age,
    major: student.major
  }
  // 滚动到表单位置
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/**
 * 取消编辑
 */
const cancelEdit = () => {
  resetForm()
}

/**
 * 删除学生
 */
const deleteStudent = async (id) => {
  // 确认删除
  if (!confirm('确定要删除这个学生吗？')) {
    return
  }
  try {
    // 发送DELETE请求
    await axios.delete(`${API_URL}${id}/`)
    alert('删除成功')
    // 重新获取学生列表
    await fetchStudents()
  } catch (error) {
    console.error('删除失败:', error)
    alert('删除失败')
  }
}

/**
 * 重置表单
 */
const resetForm = () => {
  form.value = {
    name: '',
    age: '',
    major: ''
  }
  editingId.value = null
}

/**
 * 组件挂载时获取学生列表
 */
onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
/* 主容器样式 */
.container {
  max-width: 1000px;
  margin: 0 auto;
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* 标题样式 */
h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

h2 {
  color: #555;
  margin-bottom: 20px;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

/* 表单容器样式 */
.form-box {
  margin-bottom: 40px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 5px;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: inline-block;
  width: 80px;
  font-weight: bold;
  color: #555;
}

.form-group input {
  width: calc(100% - 90px);
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #4CAF50;
}

/* 按钮容器 */
.form-buttons {
  margin-top: 20px;
}

/* 按钮基础样式 */
.btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-right: 10px;
}

/* 主要按钮（添加/更新） */
.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

/* 次要按钮（取消） */
.btn-secondary {
  background-color: #999;
  color: white;
}

.btn-secondary:hover {
  background-color: #888;
}

/* 编辑按钮 */
.btn-edit {
  background-color: #2196F3;
  color: white;
}

.btn-edit:hover {
  background-color: #0b7dda;
}

/* 删除按钮 */
.btn-delete {
  background-color: #f44336;
  color: white;
}

.btn-delete:hover {
  background-color: #da190b;
}

/* 表格容器 */
.table-box {
  margin-top: 20px;
}

/* 空数据提示 */
.empty-text {
  text-align: center;
  color: #999;
  padding: 40px 0;
}

/* 表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
}

tr:hover {
  background-color: #f5f5f5;
}

td button {
  margin-right: 5px;
}
</style>
