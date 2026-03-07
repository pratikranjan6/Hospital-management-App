<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8 col-lg-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h2 class="h4 mb-0">Add a new Doctor</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="submitDoctor">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input 
                  v-model="formData.username"
                  type="email" 
                  id="username"
                  class="form-control"
                  placeholder="Enter doctor's username"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  v-model="formData.password"
                  type="password" 
                  id="password"
                  class="form-control"
                  placeholder="Enter a password"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="fullname" class="form-label">Fullname</label>
                <input 
                  v-model="formData.name"
                  type="text" 
                  id="fullname"
                  class="form-control"
                  placeholder="Enter doctor's full name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="specialization" class="form-label">Specialization/Department</label>
                <select 
                  v-model="formData.specialization"
                  id="specialization"
                  class="form-select"
                  required
                >
                  <option value="">Select Department</option>
                  <option v-for="dept in departments" :key="dept.id" :value="dept.id">
                    {{ dept.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="qualification" class="form-label">Qualification</label>
                <input 
                  v-model="formData.qualification"
                  type="text" 
                  id="qualification"
                  class="form-control"
                  placeholder="e.g., MBBS, MD, etc."
                  required
                />
              </div>
              <div class="mb-3">
                <label for="experience" class="form-label">Experience (years)</label>
                <input 
                  v-model="formData.experience"
                  type="number" 
                  id="experience"
                  class="form-control"
                  placeholder="Enter years of experience"
                  required
                />
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Create</button>
              </div>
            </form>
            <button @click="router.push('/admin_dashboard')" class="btn btn-secondary w-100 mt-3">Back</button>
          </div>
        </div>
      </div>
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
