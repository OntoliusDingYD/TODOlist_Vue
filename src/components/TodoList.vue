<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface TodoItem {
  id: number
  title: string
  completed: boolean
  created_at: string
  due_time: string
}

const todos = ref<TodoItem[]>([])
const newTodo = ref('')
const newDueTime = ref('')  // 新增截止时间输入
const isLoading = ref(false)
const error = ref('')

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 5000
})

// 截止时间渐变色算法
function getDueTimeColor(dueTime: string): string {
  const now = new Date()
  const due = new Date(dueTime)
  const diffHour = (due.getTime() - now.getTime()) / (60*60*1000)   // 此处Date.getTime()单位是毫秒
  if (diffHour < 0) {
    // 已经过期，深红色
    const overdueDays = Math.abs(diffHour) / 24 // 过期天数
    const overdueIntensity = Math.min(overdueDays / 7, 1)   // 7天后达到最深色
    return `hsl(0, 80%, ${50 - overdueIntensity * 30}%)`  // 根据过期天数动态调整红色亮度，从50%到20%
  }

  // 尚未过期，将时间差映射到0-1
  const maxComfortableHours = 7 * 24;   // 最大小时数
  let ratio = Math.min(diffHour / maxComfortableHours, 1)

  ratio = 1 - Math.pow(1-ratio, 2)  // 平方根缓动平滑过渡，避免过于突兀

  const hue = ratio * 120
  const saturation = 70 + ratio * 10
  const lightness = 45 + ratio * 15

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`
}

function getDueTimeStyle(dueTime: string) {
  const now = new Date()
  const due = new Date(dueTime)
  const isOverdue = due < now

  return {
    color: getDueTimeColor(dueTime),
    fontWeight: isOverdue ? 'bold' : 'normal',
    textShadow: isOverdue ? '0 0 3px rgba(139, 0, 0, 0.5)' : 'none'
  }
}


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

function getCurrentDateTime() {
  const now = new Date()
  // 转换为本地时间的 datetime-local 格式
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

function clearDueTime() {
  newDueTime.value = ''
}

// 修改addTodo函数，不转换为UTC
async function addTodo() {
  if (!newTodo.value.trim()) return
  
  try {
    const payload: any = {
      title: newTodo.value.trim()
    }
    
    // 如果有设置截止时间，直接发送本地时间
    if (newDueTime.value) {
      // 不调用toISOString()，直接发送本地时间字符串
      payload.due_time = newDueTime.value  // datetime-local的值已经是本地时间格式
      console.log('发送的截止时间（本地时间）:', payload.due_time)
    } else {
      console.log('没有设置截止时间，将使用默认值')
    }
    
    console.log('发送的payload:', payload)
    
    const { data } = await api.post('/todos', payload)
    console.log('服务器返回的数据:', data)
    
    todos.value.push(data)
    newTodo.value = ''
    newDueTime.value = ''
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
        class="todo-input"
      />
      <div class="datetime-wrapper">
        <label for="due-time">Due:</label>
        <input 
          id="due-time"
          v-model="newDueTime"
          type="datetime-local"
          class="due-time-input"
          :min="getCurrentDateTime()"
        />
        <!-- 预留固定空间给清除按钮 -->
        <div class="clear-btn-container">
          <button 
            @click="clearDueTime" 
            class="clear-btn" 
            v-show="newDueTime" 
            title="Clear due time"
          >✕</button>
        </div>
      </div>
      <button @click="addTodo" class="add-btn">Add</button>
      <button @click="clearAllTodos" class="clear-all-btn">Clear All</button>
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
        <div class="todo-dates">
          <span class="todo-date created">{{ new Date(todo.created_at).toLocaleString() }}</span>
          <span class="todo-date due"
          :style="getDueTimeStyle(todo.due_time)"
          >
            {{ new Date(todo.due_time).toLocaleString() }}
          </span>
        </div>
        <button @click="removeTodo(todo.id)">×</button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.todo-container {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  background-color: #34495e;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* 输入组布局 */
.input-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
  flex-wrap: nowrap;
  min-width: 0;
}

.todo-input {
  flex: 2;
  min-width: 200px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #bdc3c7;
  border-radius: 6px;
  background-color: #ecf0f1;
}

.datetime-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background-color: #2c3e50;
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #34495e;
  min-width: 220px;
}

.datetime-wrapper label {
  color: #ecf0f1;
  font-size: 14px;
  white-space: nowrap;
}

.due-time-input {
  padding: 6px;
  border: 1px solid #bdc3c7;
  border-radius: 4px;
  font-size: 14px;
  background-color: white;
  flex: 1;
  min-width: 150px;
}

/* 清除按钮容器 */
.clear-btn-container {
  width: 24px;
  height: 24px;
  position: relative;
  flex-shrink: 0;
}

.clear-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
}

.clear-btn:hover {
  background-color: #c0392b;
}

.add-btn, .clear-all-btn {
  flex-shrink: 0;
  white-space: nowrap;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.add-btn {
  background-color: #27ae60;
  color: white;
}

.clear-all-btn {
  background-color: #e74c3c;
  color: white;
}

/* TODO列表样式 */
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

/* 时间显示样式 */
.todo-dates {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-left: 10px;
  min-width: 160px;
}

.todo-date {
  font-size: 0.75em;
  color: #7f8c8d;
  white-space: nowrap;
  line-height: 1.2;
}

.todo-date.created {
  color: #ffd700;
}

/* 完成状态样式 */
.completed {
  text-decoration: line-through;
  color: #a8a8a8;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .input-group {
    flex-wrap: wrap;
  }
  
  .todo-input {
    flex: 1 1 100%;
    margin-bottom: 10px;
  }
  
  .datetime-wrapper {
    flex: 1 1 auto;
  }
}

.debug-context {
  font-size: 0.6em;
  color: #00ff14; /* 绿色调试信息 */
}
</style>
