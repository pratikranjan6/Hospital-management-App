<template>
    <div class="register-container">
        <div class="register-page">
            <h1>� Welcome to Hospital Management</h1>
            <h2>📝 Register</h2>

            <form @submit.prevent="submit">
                <div class="form-group">
                    <label for="username">📧 Username (Email)</label>
                    <input id="username" v-model="form.username" type="email" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="full_name">👤 Full Name</label>
                    <input id="full_name" v-model="form.full_name" type="text" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="password">🔑 Password</label>
                    <input id="password" v-model="form.password" type="password" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="address">🏠 Address</label>
                    <input id="address" v-model="form.address" type="text" class="form-control" required />
                </div>

                <div class="form-group">
                    <label for="pin_code">📍 Pin Code</label>
                    <input id="pin_code" v-model="form.pin_code" type="text" class="form-control" required />
                </div>

                <div class="actions mt-3">
                    <button type="submit" class="btn btn-primary" :disabled="loading">
                        {{ loading ? '⏳ Registering...' : ' Register' }}
                    </button>
                    <button type="button" class="btn btn-success" @click="goLogin">
                         Existing user
                    </button>
                </div>
            </form>

            <div v-if="error" class="mt-3 error-message">⚠️ {{ error }}</div>
            <div v-if="success" class="mt-3 success-message">✅ {{ success }}</div>
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

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.register-page {
  max-width: 500px;
  width: 100%;
  background-color: #ffffff;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.register-page h1 {
  color: #324e6a;
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  text-align: center;
}

.register-page h2 {
  color: #667eea;
  font-size: 1.3rem;
  margin-bottom: 2rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.25rem;
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
  font-family: inherit;
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

.success-message {
  color: #22863a;
  background-color: #f0f8ff;
  border-left: 4px solid #28a745;
  padding: 1rem;
  border-radius: 4px;
  font-weight: 500;
}

.mt-3 {
  margin-top: 1.5rem;
}
</style>
