<template>
  <div class="container d-flex align-items-center justify-content-center min-vh-100">
    <div class="card shadow" style="max-width: 500px; width: 100%;">
      <div class="card-body p-4">
        <h2 class="card-title text-center mb-3">Welcome to Hospital Management</h2>
        <h2 class="h4 text-center mb-4">📝 Register</h2>

        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="username" class="form-label">📧 Username (Email)</label>
            <input id="username" v-model="form.username" type="email" class="form-control" required />
          </div>

          <div class="mb-3">
            <label for="full_name" class="form-label">👤 Full Name</label>
            <input id="full_name" v-model="form.full_name" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">🔑 Password</label>
            <input id="password" v-model="form.password" type="password" class="form-control" required />
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">🏠 Address</label>
            <input id="address" v-model="form.address" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label for="pin_code" class="form-label">📍 Pin Code</label>
            <input id="pin_code" v-model="form.pin_code" type="text" class="form-control" required />
          </div>

          <div class="d-grid gap-2 mt-4">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '⏳ Registering...' : 'Register' }}
            </button>
            <button type="button" class="btn btn-success" @click="goLogin">
              Existing user
            </button>
          </div>
        </form>

        <div v-if="error" class="alert alert-danger mt-3">⚠️ {{ error }}</div>
        <div v-if="success" class="alert alert-success mt-3">✅ {{ success }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { getApiBase } from '../utils/auth'

const form = reactive({ username: '', full_name: '', password: '', address: '', pin_code: '' })
const loading = ref(false)
const error = ref('')
const success = ref('')

const router = useRouter()

function goLogin() {
    router.push('/login')
}

async function submit() {
    error.value = ''
    success.value = ''
    loading.value = true

    if (!form.username || !form.full_name || !form.password || !form.address || !form.pin_code) {
        error.value = 'Please fill in all required fields.'
        loading.value = false
        return
    }

    try {
        const res = await axios.post(`${getApiBase()}/api/register`, {
            username: form.username,
            full_name: form.full_name,
            password: form.password,
            address: form.address,
            pin_code: form.pin_code
        }, { headers: { 'Content-Type': 'application/json' } })

        if (res.status === 201 || res.data?.msg) {
            success.value = res.data?.msg || 'Registered successfully.'
            setTimeout(() => { router.push('/login') }, 900)
        } else {
            error.value = 'Registration failed.'
        }
    } catch (err) {
        error.value = err.response?.data?.msg || err.response?.data?.message || err.message || 'Registration failed.'
    } finally {
        loading.value = false
    }
}
</script>
