<template>
  <div class="register-wrapper">
    <!-- Navbar -->
    <nav class="navbar-top">
      <div class="navbar-container">
        <div class="logo-section">
          <span class="logo"> MediCare</span>
        </div>
        <div class="nav-info">
          <span class="nav-text">Already have an account? <router-link to="/login" class="signin-link">Sign In</router-link></span>
        </div>
      </div>
    </nav>

    <!-- Main Register Container -->
    <div class="register-container">
      <!-- Left Side - Background Image -->
      <div class="left-section">
        <div class="background-content">
          <div class="content-overlay">
            <h1 class="left-title">Join MediCare</h1>
            <p class="left-subtitle">Create Your Health Profile Today</p>
            <p class="left-description">Register with us to manage your health records, book appointments with doctors, and receive personalized healthcare recommendations all in one place.</p>
          </div>
        </div>
      </div>

      <!-- Right Side - Register Form -->
      <div class="right-section">
        <div class="form-container">
          <h2 class="form-title">Sign up with your Email</h2>
          <p class="form-subtitle">Create your MediCare account in just a few steps</p>

          <!-- Register Form -->
          <form @submit.prevent="submit">
            <!-- Email -->
            <div class="form-group">
              <label for="username" class="form-label">Email Address</label>
              <input 
                id="username" 
                v-model="form.username" 
                type="email" 
                class="form-input" 
                placeholder="Enter your email"
                required 
              />
            </div>

            <!-- Full Name -->
            <div class="form-group">
              <label for="full_name" class="form-label">Full Name</label>
              <input 
                id="full_name" 
                v-model="form.full_name" 
                type="text" 
                class="form-input" 
                placeholder="Enter your full name"
                required 
              />
            </div>

            <!-- Password -->
            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <input 
                id="password" 
                v-model="form.password" 
                type="password" 
                class="form-input" 
                placeholder="Enter your password"
                required 
              />
            </div>

            <!-- Address -->
            <div class="form-group">
              <label for="address" class="form-label">Address</label>
              <input 
                id="address" 
                v-model="form.address" 
                type="text" 
                class="form-input" 
                placeholder="Enter your address"
                required 
              />
            </div>

            <!-- Pin Code -->
            <div class="form-group">
              <label for="pin_code" class="form-label">Pin Code</label>
              <input 
                id="pin_code" 
                v-model="form.pin_code" 
                type="text" 
                class="form-input" 
                placeholder="Enter your pin code"
                required 
              />
            </div>

            <!-- Error Message -->
            <div v-if="error" class="alert alert-error">
              ✕ {{ error }}
            </div>

            <!-- Success Message -->
            <div v-if="success" class="alert alert-success">
              ✓ {{ success }}
            </div>

            <!-- Sign Up Button -->
            <button type="submit" class="sign-up-btn" :disabled="loading">
              {{ loading ? 'Creating account...' : 'Sign Up' }}
            </button>
          </form>

          <!-- Sign In Link -->
          <p class="signin-prompt">
            Already have an account? 
            <router-link to="/login" class="signin-link-bottom">Sign In</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { getApiBase } from '../utils/auth'

const form = reactive({ 
  username: '', 
  full_name: '', 
  password: '', 
  address: '', 
  pin_code: '' 
})
const loading = ref(false)
const error = ref('')
const success = ref('')

const router = useRouter()

async function submit() {
    error.value = ''
    success.value = ''
    loading.value = true

    if (!form.username || !form.full_name || !form.password || !form.address || !form.pin_code) {
        error.value = 'Please fill in all required fields.'
        loading.value = false
        return
    }

    if (form.password.length < 6) {
        error.value = 'Password must be at least 6 characters long.'
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
            success.value = res.data?.msg || 'Account created successfully! Redirecting to login...'
            setTimeout(() => { router.push('/login') }, 1500)
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.register-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: #f5f7fa;
}

/* ========== NAVBAR ========== */
.navbar-top {
  background: white;
  border-bottom: 1px solid #e0e0e0;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #007bff;
  cursor: pointer;
  transition: color 0.3s ease;
}

.logo:hover {
  color: #0056b3;
}

.nav-info {
  display: flex;
  align-items: center;
}

.nav-text {
  color: #666;
  font-size: 0.95rem;
}

.signin-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.5rem;
  transition: color 0.3s ease;
}

.signin-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* ========== REGISTER CONTAINER ========== */
.register-container {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  overflow: hidden;
}

/* Left Section */
.left-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  overflow: hidden;
}

.left-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 500px;
  height: 500px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;
}

.left-section::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -5%;
  width: 400px;
  height: 400px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  animation: float 8s ease-in-out infinite reverse;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(30px);
  }
}

.background-content {
  position: relative;
  z-index: 2;
  text-align: center;
}

.content-overlay {
  animation: slideInLeft 0.8s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.left-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.left-subtitle {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
  font-weight: 600;
}

.left-description {
  font-size: 1rem;
  opacity: 0.8;
  line-height: 1.6;
  max-width: 350px;
}

/* Right Section */
.right-section {
  background: white;
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.form-container {
  width: 100%;
  max-width: 400px;
  animation: slideInRight 0.8s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.form-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.form-subtitle {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

/* Form */
.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  color: black;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: #f9f9f9;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #999;
}

/* Alerts */
.alert {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  animation: slideInDown 0.3s ease-out;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.alert-error {
  background: #fee;
  color: #c00;
  border: 1px solid #fcc;
}

.alert-success {
  background: #efe;
  color: #060;
  border: 1px solid #cfc;
}

/* Sign Up Button */
.sign-up-btn {
  width: 100%;
  padding: 0.9rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  margin-top: 0.5rem;
}

.sign-up-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.sign-up-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sign-up-btn:active:not(:disabled) {
  transform: translateY(0);
}

/* Sign In Prompt */
.signin-prompt {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.signin-link-bottom {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.signin-link-bottom:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 992px) {
  .register-container {
    grid-template-columns: 1fr;
  }

  .left-section {
    display: none;
  }

  .right-section {
    padding: 2rem;
  }

  .form-container {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    padding: 0 1rem;
    flex-direction: column;
    gap: 0.5rem;
  }

  .nav-info {
    font-size: 0.85rem;
  }

  .right-section {
    padding: 1.5rem;
  }

  .form-title {
    font-size: 1.5rem;
  }

  .form-input {
    padding: 0.65rem 0.9rem;
    color: black;
  }

  .form-group {
    margin-bottom: 0.8rem;
  }
}

@media (max-width: 480px) {
  .navbar-top {
    padding: 0.75rem 0;
  }

  .navbar-container {
    padding: 0 1rem;
  }

  .logo {
    font-size: 1.2rem;
  }

  .nav-text {
    display: none;
  }

  .right-section {
    padding: 1rem;
  }

  .form-container {
    padding: 0;
  }

  .form-title {
    font-size: 1.3rem;
  }

  .form-subtitle {
    font-size: 0.85rem;
  }

  .left-title {
    font-size: 1.8rem;
  }

  .left-subtitle {
    font-size: 1.1rem;
  }

  .form-group {
    margin-bottom: 0.7rem;
  }

  .form-input {
    padding: 0.6rem 0.8rem;
    font-size: 0.9rem;
  }

  .form-label {
    font-size: 0.85rem;
  }
}
</style>
