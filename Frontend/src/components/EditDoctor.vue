<template>
  <div class="admin-wrapper">
    <AdminNavBar />
    
    <div class="admin-container">
      <div class="form-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title"> Edit Doctor</h2>
            <p class="card-subtitle">Update doctor information</p>
          </div>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="submitEdit" class="form-grid">
            <div class="form-group">
              <label for="name" class="form-label">Full Name</label>
              <input 
                v-model="formData.name" 
                id="name" 
                type="text" 
                class="form-input" 
                placeholder="Enter doctor's full name"
                required 
              />
            </div>

            <div class="form-group">
              <label class="form-label">Specialization/Department</label>
              <input 
                :value="specializationName" 
                class="form-input form-input-disabled" 
                disabled 
                readonly 
              />
              <p class="field-note">Department cannot be changed</p>
            </div>

            <div class="form-group">
              <label for="qualification" class="form-label">Qualification</label>
              <input 
                v-model="formData.qualification" 
                id="qualification" 
                type="text" 
                class="form-input"
                placeholder="e.g., MBBS, MD, etc."
                required 
              />
            </div>

            <div class="form-group">
              <label for="experience" class="form-label">Experience (years)</label>
              <input 
                v-model.number="formData.experience" 
                id="experience" 
                type="number" 
                min="0" 
                class="form-input"
                placeholder="Enter years of experience"
                required 
              />
            </div>

            <div class="button-group">
              <button type="submit" class="btn-submit">Update Doctor</button>
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
import { useRouter, useRoute } from 'vue-router'
import AdminNavBar from './AdminNavBar.vue'
import { getApiBase } from '../utils/auth'

const router = useRouter()
const route = useRoute()
const API_BASE = getApiBase()

const formData = ref({
  name: '',
  qualification: '',
  experience: 0
})

const specializationName = ref('')

async function fetchDoctor() {
  try {
    const token = localStorage.getItem('token')
    const resp = await axios.get(`${API_BASE}/api/admin/doctors`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    const doctors = resp.data || []
    const id = parseInt(route.params.id)
    const doc = doctors.find(d => d.id === id)
    if (!doc) {
      alert('Doctor not found')
      router.push('/admin_dashboard')
      return
    }
    formData.value.name = doc.name || ''
    formData.value.qualification = doc.qualification || ''
    formData.value.experience = doc.experience || 0
    specializationName.value = doc.specialization || ''
  } catch (err) {
    console.error('Failed to fetch doctor:', err)
    alert('Failed to load doctor data')
    router.push('/admin_dashboard')
  }
}

async function submitEdit() {
  try {
    const token = localStorage.getItem('token')
    const id = route.params.id
    await axios.put(`${API_BASE}/api/admin/doctor/${id}`,
      {
        name: formData.value.name,
        qualification: formData.value.qualification,
        experience: formData.value.experience
      },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    alert('Doctor updated successfully')
    router.push('/admin_dashboard')
  } catch (err) {
    console.error('Failed to update doctor:', err)
    alert('Error updating doctor: ' + (err.response?.data?.msg || err.message))
  }
}

onMounted(() => {
  fetchDoctor()
})
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
  background: #f2e8d8;
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
  background: #fffdf7;
  border-radius: 24px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  animation: slideUp 0.5s ease-out;
  border-top: 4px solid #8f7b65;
  border: 1px solid #d8c8b0;
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
  background: #f4e9db;
  color: #3d362f;
  border-bottom: 1px solid #dacbb8;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -0.02em;
}

.card-subtitle {
  font-size: 0.95rem;
  color: #7d6d5f;
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
  font-weight: 700;
  color: #3d362f;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 2px solid #d8c8b0;
  border-radius: 16px;
  color: #3d362f;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #fff9f1;
}

.form-input:focus {
  outline: none;
  border-color: #8f7b65;
  box-shadow: 0 0 0 3px rgba(143, 123, 101, 0.15);
  background: #fffdf7;
}

.form-input::placeholder {
  color: #bfafa1;
}

.form-input-disabled {
  background: #f0e5d8;
  color: #7d6d5f;
  cursor: not-allowed;
  border-color: #d8c8b0;
}

.form-input-disabled:focus {
  border-color: #d8c8b0;
  box-shadow: none;
  background: #f0e5d8;
}

.field-note {
  font-size: 0.8rem;
  color: #7d6d5f;
  margin: 0;
  margin-top: -0.3rem;
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
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-submit {
  background: #8f7b65;
  color: white;
}

.btn-submit:hover {
  transform: translateY(-2px);
  background: #7a6a58;
  box-shadow: 0 8px 20px rgba(143, 123, 101, 0.3);
}

.btn-submit:active {
  transform: translateY(0);
}

.btn-back {
  background: #f4e9db;
  color: #3d362f;
  border: 2px solid #d8c8b0;
}

.btn-back:hover {
  background: #e6d9c8;
  border-color: #8f7b65;
  color: #8f7b65;
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
