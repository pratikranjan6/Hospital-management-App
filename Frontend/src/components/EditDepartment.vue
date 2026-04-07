<template>
  <div class="admin-wrapper">
    <AdminNavBar />
    
    <div class="admin-container">
      <div class="form-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title"> Edit Department</h2>
            <p class="card-subtitle">Update department information</p>
          </div>
        </div>
        
        <div class="card-body">
          <form @submit.prevent="submitEdit" class="form-grid">
            <div class="form-group">
              <label for="name" class="form-label">Department Name</label>
              <input 
                v-model="formData.name" 
                id="name" 
                type="text" 
                class="form-input"
                placeholder="Enter department name"
                required 
              />
            </div>

            <div class="form-group">
              <label for="description" class="form-label">Description</label>
              <textarea 
                v-model="formData.description" 
                id="description" 
                rows="6"
                class="form-input form-textarea"
                placeholder="Enter department description"
                required
              ></textarea>
            </div>

            <div class="button-group">
              <button type="submit" class="btn-submit">Update Department</button>
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
import { getApiBase, getAuthHeader } from '../utils/auth'

const router = useRouter()
const route = useRoute()
const API_BASE = getApiBase()

const formData = ref({ name: '', description: '' })

async function fetchDepartment() {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const resp = await axios.get(`${API_BASE}/api/departments`, { headers: auth })
    const departments = resp.data || []
    const id = parseInt(route.params.id)
    const dept = departments.find(d => d.id === id)
    if (!dept) {
      alert('Department not found')
      router.push('/admin_dashboard')
      return
    }
    formData.value.name = dept.name || ''
    formData.value.description = dept.description || ''
  } catch (err) {
    console.error('Failed to load department:', err)
    alert('Failed to load department')
    router.push('/admin_dashboard')
  }
}

async function submitEdit() {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const id = route.params.id
    await axios.put(`${API_BASE}/api/admin/department/${id}`,
      {
        name: formData.value.name,
        description: formData.value.description
      },
      { headers: auth }
    )
    alert('Department updated')
    router.push('/admin_dashboard')
  } catch (err) {
    console.error('Failed to update department:', err)
    alert('Error updating department: ' + (err.response?.data?.msg || err.message))
  }
}

onMounted(() => fetchDepartment())
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
  border-top: 4px solid #f093fb;
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
  color: black;
  border-radius: 8px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #fff;
  resize: none;
}

.form-input:focus {
  outline: none;
  border-color: #f093fb;
  box-shadow: 0 0 0 3px rgba(240, 147, 251, 0.1);
  background: #fff9fd;
}

.form-input::placeholder {
  color: #b0bcc4;
}

.form-textarea {
  min-height: 150px;
  line-height: 1.5;
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
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(240, 147, 251, 0.3);
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
  border-color: #f093fb;
  color: #f093fb;
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
