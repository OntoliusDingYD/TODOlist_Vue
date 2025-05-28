<script setup lang="ts">
import { ref } from 'vue'
import HelloWorld from './components/HelloWorld.vue'
import TodoList from './components/TodoList.vue';
import axios from 'axios';

const isUnlocked = ref(false)
const unlockApp = () => {
  isUnlocked.value = true
}
</script>

<template>
  <div class="app-container">
    <HelloWorld 
      msg="TODO list by Ontolius" 
      :is-unlocked="isUnlocked"
      @unlock="unlockApp" 
    />
    <TodoList v-if="isUnlocked" />
  </div>
</template>

<style>
/* 全局样式 */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 20px;
  background-color: #2c3e50;
  color: #ecf0f1;
}

.app-container {
  max-width: 800px;
  margin: 0 auto;
}

/* 保留原有的logo样式 */
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
