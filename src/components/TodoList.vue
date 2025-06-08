<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface TodoItem {
  id: number
  title: string
  completed: boolean
  created_at: string
}

const todos = ref<TodoItem[]>([])
const newTodo = ref('')
const isLoading = ref(false)
const error = ref('')

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000
})

// 从API加载数据
const loadTodos = async () => {
  try {
    isLoading.value = true
    const { data } = await api.get('/todos')
    todos.value = data
  } catch (err) {
    error.value = axios.isAxiosError(err) 
      ? err.message
      : 'Unknown error'
  } finally {
    isLoading.value = false
  }
}

// 初始化加载
onMounted(() => {
  loadTodos()
})

async function addTodo() {
  if (!newTodo.value.trim()) return
  
  try {
    const { data } = await api.post('/todos', {
      title: newTodo.value.trim()
    })
    todos.value.push(data)
    newTodo.value = ''
  } catch (err) {
    error.value = axios.isAxiosError(err)
      ? err.message
      : 'Failed to add todo'
  }
}

async function removeTodo(id: number) {
  try {
    await api.delete(`/todos/${id}`)
    todos.value = todos.value.filter(todo => todo.id !== id)
  } catch (err) {
    error.value = axios.isAxiosError(err)
      ? err.message
      : 'Failed to delete todo'
  }
}

function toggleTodo(id: number) {
  const todo = todos.value.find(t => t.id === id)
  if (todo) {
    todo.completed = !todo.completed
    // 注意: 这里简化了实现，实际应该调用API更新状态
  }
}

function clearAllTodos() {
  // 注意: 这里简化了实现，实际应该逐个调用API删除
  todos.value = []
}
</script>

<template>
  <div class="todo-container">
    <h2>TODO List</h2>
    <div class="input-group">
      <input 
        v-model="newTodo"
        @keyup.enter="addTodo"
        placeholder="Add new todo..."
      />
      <button @click="addTodo">Add</button>
      <button @click="clearAllTodos" style="margin-left: 10px;">Clear All</button>
    </div>
    <ul class="todo-list">
      <li v-for="todo in todos" :key="todo.id">
        <input 
          type="checkbox" 
          :checked="todo.completed"
          @change="toggleTodo(todo.id)"
        />
        <span class="todo-id">#{{ todo.id }}</span>
        <span :class="{ completed: todo.completed }">{{ todo.title }}</span>
        <span class="todo-date">{{ new Date(todo.created_at).toLocaleString() }}</span>
        <button @click="removeTodo(todo.id)">×</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.todo-container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  background-color: #34495e;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.input-group {
  display: flex;
  margin-bottom: 20px;
}
.input-group input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
}
.input-group button {
  margin-left: 10px;
  padding: 8px 16px;
}
.todo-list {
  list-style: none;
  padding: 0;
}
.todo-list li {
  display: flex;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #4a6278;
  color: #ecf0f1;
}
.todo-list li span {
  margin: 0 10px;
}
.todo-list li .todo-id {
  color: #7f8c8d;
  font-size: 0.8em;
  min-width: 50px;
}
.todo-list li span:not(.todo-id, .todo-date) {
  flex: 1;
}
.todo-date {
  font-size: 0.8em;
  color: #7f8c8d;
  margin-left: 10px;
}
.completed {
  text-decoration: line-through;
  color: #bdc3c7;
}
</style>
