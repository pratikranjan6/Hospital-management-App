<template>
  <div class="login-wrapper">
    <!-- Navbar -->
    <nav class="navbar-top">
      <div class="navbar-container">
        <div class="logo-section">
          <span class="logo"> MediCare</span>
        </div>
        <div class="nav-info">
          <span class="nav-text">Don't have an account? <router-link to="/register" class="signup-link">Sign Up</router-link></span>
        </div>
      </div>
    </nav>

    <!-- Main Login Container -->
    <div class="login-container">
      <!-- Left Side - Background Image -->
      <div class="left-section">
        <div class="background-content">
          <div class="content-overlay">
            <h1 class="left-title">Welcome to MediCare</h1>
            <p class="left-subtitle">Your Trusted Healthcare Solution</p>
            <p class="left-description">Manage your health records, book appointments, and connect with healthcare professionals in one place.</p>
          </div>
        </div>
      </div>

      <!-- Right Side - Login Form -->
      <div class="right-section">
        <div class="form-container">
          <h2 class="form-title">Sign in to MediCare</h2>
          <p class="form-subtitle">Enter your credentials to access your account</p>

          <!-- Social Login Buttons -->
          <div class="social-login">
            <button class="social-btn google-btn" @click="handleGoogleLogin">
              <span class="google-icon"></span>
              <span>Sign in with Google</span>
            </button>
            <button class="social-btn microsoft-btn" @click="handleMicrosoftLogin">
              <span class="microsoft-icon"></span>
              <span>Sign in with Microsoft</span>
            </button>
          </div>

          <!-- Divider -->
          <div class="divider">
            <span>Or continue with email</span>
          </div>

          <!-- Login Form -->
          <form @submit.prevent="submit">
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

            <!-- Forgot Password Link -->
            <div class="forgot-password">
              <router-link to="/forgot" class="forgot-link">Forgot your password?</router-link>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="alert alert-error">
              ✕ {{ error }}
            </div>

            <!-- Sign In Button -->
            <button type="submit" class="sign-in-btn" :disabled="loading">
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>

          <!-- Sign Up Link -->
          <p class="signup-prompt">
            Need a MediCare account? 
            <router-link to="/register" class="signup-link-bottom">Sign Up</router-link>
          </p>
        </div>
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

// Social Login Handlers (Demo)
function handleGoogleLogin() {
  alert('Google login integration coming soon! Backend authentication needed.')
  // In future: integrate Google OAuth
}

function handleMicrosoftLogin() {
  alert('Microsoft login integration coming soon! Backend authentication needed.')
  // In future: integrate Microsoft OAuth
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-wrapper {
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

.signup-link {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
  margin-left: 0.5rem;
  transition: color 0.3s ease;
}

.signup-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* ========== LOGIN CONTAINER ========== */
.login-container {
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

/* Social Login */
.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
}

.social-btn:hover {
  border-color: #667eea;
  background: #f5f7fa;
  transform: translateY(-2px);
}

.google-icon,
.microsoft-icon {
  font-size: 1.2rem;
}

/* Divider */
.divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
  color: #999;
  font-size: 0.85rem;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #e0e0e0;
}

.divider::before {
  margin-right: 1rem;
}

.divider::after {
  margin-left: 1rem;
}

/* Form */
.form-group {
  margin-bottom: 1.2rem;
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

/* Forgot Password */
.forgot-password {
  text-align: right;
  margin-bottom: 1.5rem;
}

.forgot-link {
  color: #007bff;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* Alert */
.alert {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.alert-error {
  background: #fee;
  color: #c00;
  border: 1px solid #fcc;
}

/* Sign In Button */
.sign-in-btn {
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
}

.sign-in-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.sign-in-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sign-in-btn:active:not(:disabled) {
  transform: translateY(0);
}

/* Sign Up Prompt */
.signup-prompt {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
  font-size: 0.9rem;
}

.signup-link-bottom {
  color: #007bff;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.signup-link-bottom:hover {
  color: #0056b3;
  text-decoration: underline;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 992px) {
  .login-container {
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

  .social-login {
    grid-template-columns: 1fr;
  }

  .social-btn {
    text-align: center;
  }

  .form-input {
    padding: 0.65rem 0.9rem;
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
}
</style>