<template>
  <div class="add-doctor-container">
    <!-- Header -->
    <div class="form-section">
      <h2>Add a new Doctor</h2>
      <form @submit.prevent="submitDoctor" class="doctor-form">
        
        <!-- Fullname Field -->
        <div class="form-group">
          <label for="fullname">Fullname</label>
          <input 
            v-model="formData.name"
            type="text" 
            id="fullname"
            placeholder="Enter doctor's full name"
            required
          />
        </div>

        <!-- Specialization/Department Field -->
        <div class="form-group">
          <label for="specialization">Specialization/Department</label>
          <select 
            v-model="formData.specialization"
            id="specialization"
            required
          >
            <option value="">Select Department</option>
            <option v-for="dept in departments" :key="dept.id" :value="dept.id">
              {{ dept.name }}
            </option>
          </select>
        </div>

        <!-- Qualification Field -->
        <div class="form-group">
          <label for="qualification">Qualification</label>
          <input 
            v-model="formData.qualification"
            type="text" 
            id="qualification"
            placeholder="e.g., MBBS, MD, etc."
            required
          />
        </div>

        <!-- Experience Field -->
        <div class="form-group">
          <label for="experience">Experience (years)</label>
          <input 
            v-model="formData.experience"
            type="number" 
            id="experience"
            placeholder="Enter years of experience"
            required
          />
        </div>

        <!-- Availability Field -->
        <div class="form-group">
          <label for="availability">Availability</label>
          <input 
            v-model="formData.availability"
            type="text" 
            id="availability"
            placeholder="e.g., Mon-Fri, 9AM-5PM"
            required
          />
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn-create">Create</button>
      </form>
      <p class="note">Note: Students can add more fields if required</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { getApiBase } from '../utils/auth'

const router = useRouter()
const API_BASE = getApiBase()

const formData = ref({
  name: '',
  specialization: '',
  qualification: '',
  experience: '',
  availability: ''
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
.add-doctor-container {
  padding: 40px;
  background: #f5f5f5;
  min-height: 100vh;
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

.doctor-form {
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
.form-group select {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.2);
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
