<template>
  <div class="container d-flex align-items-center justify-content-center min-vh-100">
    <div class="card shadow" style="max-width: 400px; width: 100%;">
      <div class="card-body p-4">
        <h2 class="card-title text-center mb-3">Welcome to Hospital Management</h2>
        <h2 class="h4 text-center mb-4">🔐 Login</h2>

        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="username" class="form-label">📧 Username (Email Address)</label>
            <input id="username" v-model="form.username" type="email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">🔑 Password</label>
            <input id="password" v-model="form.password" type="password" class="form-control" required />
          </div>

          <div class="d-grid gap-2 mt-4">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? 'Signing in...' : 'Login' }}
            </button>
            <button type="button" class="btn btn-success" @click="goRegister">
              New user
            </button>
          </div>
        </form>

        <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { getApiBase } from '../utils/auth'

const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

const router = useRouter()
function goRegister() {
  router.push('/register')
}

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const res = await axios.post(`${getApiBase()}/api/login`, {
      username: form.value.username,
      password: form.value.password
    }, {
      headers: { 'Content-Type': 'application/json' },
      withCredentials: true
    })

    const token = res.data.access_token || res.data.token
    const role = (res.data.role || '').toLowerCase()
    if (token) {
      localStorage.setItem('token', token)
      localStorage.setItem('role', role)
      if (role === 'admin') router.push('/admin_dashboard')
      else if (role === 'doctor') router.push('/doctor_dashboard')
      else router.push('/user_dashboard')
    } else {
      error.value = res.data.msg || 'Login failed'
    }
  } catch (err) {
    error.value = err.response?.data?.msg || err.response?.data?.message || err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
<style scoped>

.mt-3 {
  margin-top: 1.5rem;
}
</style>