<script setup lang="ts">
import { ref, watch } from 'vue'

defineProps<{ 
  msg: string
  isUnlocked?: boolean
}>()

const emit = defineEmits(['unlock'])

const count = ref(0)
const target_count = Math.floor(Math.random()*1000000) + Math.floor(Math.random()*1000) + 1

watch(count, (newVal) => {
  if (newVal === target_count) {
    emit('unlock')
  }
})
</script>

<template>
  <h1>{{ msg }}</h1>
  <div v-if="!isUnlocked" style="font-size: 2em; margin-bottom: 10px;">当前值 Current Value: {{ count }}</div>
  <div v-else style="font-size: 2em; margin-bottom: 10px; color: #2ecc71;">
    成功！你已解锁 TODO List
    <br>
    Success! You unlocked the TODO List
  </div>
  <div class="card">
    <div v-if="!isUnlocked" style="font-size: 2em; margin-bottom: 10px;">
      目标 Target: {{ target_count }}
      <br>
      将值调整到目标以解锁
      <br>
      Fix Value to Target to unlock
    </div>
    <button type="button" @click="count++">+ 1</button>
    <button type="button" @click="count--">- 1</button>
    <br>
    <button type="button" @click="count = count*2">* 2</button>
    <button type="button" @click="count = Math.floor(count/2)">/ 2</button>
    <button type="button" @click="count+=Math.floor(Math.random() * 100) + 1">+ random</button>    
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>

  <p>
    Check out
    <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
      >create-vue</a
    >, the official Vue + Vite starter
  </p>
  <p>
    Learn more about IDE Support for Vue in the
    <a
      href="https://vuejs.org/guide/scaling-up/tooling.html#ide-support"
      target="_blank"
      >Vue Docs Scaling up Guide</a
    >.
  </p>
  <p class="stack-statement">Vue-Axios-Python Flask-SQLite</p>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
.stack-statement {
  color: #191981;
  font-size: 1.2em;
}
</style>
