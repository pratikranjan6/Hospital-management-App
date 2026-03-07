<template>
  <div class="add-department-container">
    <div class="form-section">
      <h2>Add a new Department</h2>
      <form @submit.prevent="submitDepartment" class="department-form">
        
        <div class="form-group">
          <label for="name">Department Name</label>
          <input 
            v-model="formData.name"
            type="text" 
            id="name"
            placeholder="Enter department name"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            v-model="formData.description"
            id="description"
            placeholder="Enter department description"
            rows="5"
            required
          ></textarea>
        </div>

        <button type="submit" class="btn-create">Create</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { getApiBase } from '../utils/auth'

const router = useRouter()
const API_BASE = getApiBase()

const formData = ref({
  name: '',
  description: ''
})

async function submitDepartment() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.post(`${API_BASE}/api/admin/department`, 
      {
        name: formData.value.name,
        description: formData.value.description
      },
      {
        headers: { 'Authorization': `Bearer ${token}` }
      }
    )
    
    alert('Department created successfully!')
    router.push('/admin_dashboard')
  } catch (error) {
    console.error('Failed to create department:', error)
    alert('Error creating department: ' + (error.response?.data?.msg || error.message))
  }
}
</script>

<style scoped>
.add-department-container {
  padding: 40px;
  background: #f5f5f5;
  min-height: 100vh;
  width: 100%;
}

.form-section {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.form-section h2 {
  color: #333;
  margin-bottom: 30px;
  text-align: center;
  font-size: 24px;
}

.department-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.form-group input,
.form-group textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.2);
}

.form-group textarea {
  resize: vertical;
}

.btn-create {
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 20px;
  transition: background 0.3s ease;
}

.btn-create:hover {
  background: #45a049;
}

.note {
  color: #666;
  font-size: 12px;
  text-align: center;
  margin-top: 20px;
}
</style>
