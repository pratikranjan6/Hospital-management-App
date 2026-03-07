<template>
  <nav class="doctor-navbar">
    <div class="nav-left">Welcome Dr. {{ username }}</div>
    <div class="nav-right">
      <button class="btn-logout" @click="logout">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref(localStorage.getItem('username') || 'Doctor')

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('role')
  router.push('/login')
}
</script>

<style scoped>
.doctor-navbar {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:12px 24px;
  background: linear-gradient(90deg,#0f1724,#102a43);
  color:#fff;
  box-shadow: 0 2px 8px rgba(2,6,23,0.2);
}
.nav-left { font-weight:600; font-size:16px }
.btn-logout { background: transparent; border:1px solid rgba(255,255,255,0.12); color:#fff; padding:8px 12px; border-radius:6px; cursor:pointer }
.btn-logout:hover { background: rgba(255,255,255,0.04) }
</style>
