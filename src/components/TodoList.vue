<script setup lang="ts">
import { ref, watch } from 'vue'

interface TodoItem {
  id: number
  text: string
  completed: boolean
}

const STORAGE_KEY = 'vue-todo-list'
const todos = ref<TodoItem[]>([])
const newTodo = ref('')

// 从本地存储加载数据
const loadTodos = () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    todos.value = JSON.parse(saved)
  }
}

// 保存数据到本地存储
const saveTodos = () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos.value))
}

// 初始化加载
loadTodos()

// 监听todos变化自动保存
watch(todos, () => {
  saveTodos()
}, { deep: true })

function addTodo() {
  if (newTodo.value.trim()) {
    todos.value.push({
      id: Date.now(),
      text: newTodo.value.trim(),
      completed: false
    })
    newTodo.value = ''
  }
}

function removeTodo(id: number) {
  todos.value = todos.value.filter(todo => todo.id !== id)
}

function toggleTodo(id: number) {
  const todo = todos.value.find(t => t.id === id)
  if (todo) {
    todo.completed = !todo.completed
  }
}

function clearAllTodos() {
  todos.value = []
  localStorage.removeItem(STORAGE_KEY)
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
        <span :class="{ completed: todo.completed }">{{ todo.text }}</span>
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
.todo-list li span:not(.todo-id) {
  flex: 1;
}
.completed {
  text-decoration: line-through;
  color: #bdc3c7;
}
</style>
