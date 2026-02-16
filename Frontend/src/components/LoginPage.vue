<template>
  <div class="login-container">
    <div class="login-page">
      <h1>� Welcome to Hospital Management</h1>
      <h2>🔐 Login</h2>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label for="username">📧 Username (Email Address)</label>
          <input id="username" v-model="form.username" type="email" class="form-control" required />
        </div>

        <div class="form-group">
          <label for="password">🔑 Password</label>
          <input id="password" v-model="form.password" type="password" class="form-control" required />
        </div>

        <div class="actions mt-3">
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? ' Signing in...' : ' Login' }}
          </button>
          <button type="button" class="btn btn-success" @click="goRegister">
             New user
          </button>
        </div>
      </form>

      <div v-if="error" class="mt-3 error-message"> {{ error }}</div>
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
      // redirect based on role using router to avoid full reload
      if (role === 'admin') router.push('/admin_dashboard')
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
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-page {
  max-width: 400px;
  width: 100%;
  background-color: #ffffff;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.login-page h1 {
  color: #324e6a;
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

.login-page h2 {
  color: #667eea;
  font-size: 1.3rem;
  margin-bottom: 2rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
  font-size: 0.95rem;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-success {
  background-color: #48bb78;
  color: white;
}

.btn-success:hover {
  background-color: #38a169;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(72, 187, 120, 0.4);
}

.error-message {
  color: #e53e3e;
  background-color: #fed7d7;
  border-left: 4px solid #e53e3e;
  padding: 1rem;
  border-radius: 4px;
  font-weight: 500;
}

.mt-3 {
  margin-top: 1.5rem;
}
</style>