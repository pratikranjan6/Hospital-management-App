<template>
  <div class="admin-wrapper">
    <AdminNavBar />
    
    <div class="admin-container">
      <div class="form-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title"> Add a new Doctor</h2>
            <p class="card-subtitle">Register a new doctor to the system</p>
          </div>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="submitDoctor" class="form-grid">
            <div class="form-group">
              <label for="username" class="form-label">Username</label>
              <input 
                v-model="formData.username"
                type="email" 
                id="username"
                class="form-input"
                placeholder="Enter doctor's username"
                required
              />
            </div>

            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <input 
                v-model="formData.password"
                type="password" 
                id="password"
                class="form-input"
                placeholder="Enter a password"
                required
              />
            </div>

            <div class="form-group">
              <label for="fullname" class="form-label">Full Name</label>
              <input 
                v-model="formData.name"
                type="text" 
                id="fullname"
                class="form-input"
                placeholder="Enter doctor's full name"
                required
              />
            </div>

            <div class="form-group">
              <label for="specialization" class="form-label">Specialization/Department</label>
              <select 
                v-model="formData.specialization"
                id="specialization"
                class="form-input"
                required
              >
                <option value="">Select Department</option>
                <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                  {{ dept.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="qualification" class="form-label">Qualification</label>
              <input 
                v-model="formData.qualification"
                type="text" 
                id="qualification"
                class="form-input"
                placeholder="e.g., MBBS, MD, etc."
                required
              />
            </div>

            <div class="form-group">
              <label for="experience" class="form-label">Experience (years)</label>
              <input 
                v-model="formData.experience"
                type="number" 
                id="experience"
                class="form-input"
                placeholder="Enter years of experience"
                required
              />
            </div>

            <div class="button-group">
              <button type="submit" class="btn-submit">Create Doctor</button>
              <button type="button" @click="router.push('/admin_dashboard')" class="btn-back">Back to Dashboard</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import AdminNavBar from './AdminNavBar.vue'
import { getApiBase } from '../utils/auth'

const router = useRouter()
const API_BASE = getApiBase()

const formData = ref({
  username: '',
  password: '',
  name: '',
  specialization: '',
  qualification: '',
  experience: '',
})

const departments = ref([])

onMounted(async () => {
  await fetchDepartments()
})

async function fetchDepartments() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_BASE}/api/departments`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    departments.value = response.data
  } catch (error) {
    console.error('Failed to fetch departments:', error)
  }
}

async function submitDoctor() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(`${API_BASE}/api/admin/doctor`, 
      {
        username: formData.value.username,
        password: formData.value.password,
        name: formData.value.name,
        specialization: parseInt(formData.value.specialization),
        qualification: formData.value.qualification,
        experience: parseInt(formData.value.experience),
        availability: formData.value.availability
      },
      {
        headers: { 'Authorization': `Bearer ${token}` }
      }
    )
    
    alert('Doctor created successfully!')
    router.push('/admin_dashboard')
  } catch (error) {
    console.error('Failed to create doctor:', error)
    alert('Error creating doctor: ' + (error.response?.data?.msg || error.message))
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.admin-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.admin-container {
  flex: 1;
  padding: 2rem;
  max-width: 700px;
  margin: 0 auto;
  width: 100%;
}

/* ========== FORM CARD ========== */
.form-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  animation: slideUp 0.5s ease-out;
  border-top: 4px solid #667eea;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.card-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin: 0;
}

.card-body {
  padding: 2rem;
}

/* ========== FORM ========== */
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e0e6ed;
  color:black;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #fff;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  background: #f8f9ff;
}

.form-input::placeholder {
  color: #b0bcc4;
}

/* ========== BUTTONS ========== */
.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-submit,
.btn-back {
  flex: 1;
  padding: 0.85rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-submit:active {
  transform: translateY(0);
}

.btn-back {
  background: #e9ecef;
  color: #2c3e50;
  border: 2px solid #dee2e6;
}

.btn-back:hover {
  background: #dee2e6;
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.btn-back:active {
  transform: translateY(0);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
  }

  .card-header {
    padding: 1.5rem;
  }

  .card-body {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.4rem;
  }

  .card-subtitle {
    font-size: 0.85rem;
  }

  .form-grid {
    gap: 1rem;
  }

  .button-group {
    flex-direction: column;
  }

  .btn-submit,
  .btn-back {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .admin-container {
    padding: 0.75rem;
  }

  .card-header {
    padding: 1rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 1.2rem;
  }

  .form-label {
    font-size: 0.9rem;
  }

  .form-input {
    font-size: 0.9rem;
    padding: 0.6rem 0.8rem;
  }

  .btn-submit,
  .btn-back {
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
