<template>
  <div class="container-fluid bg-light min-vh-100 py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Add a new Department</h2>
            <form @submit.prevent="submitDepartment">
              <div class="mb-3">
                <label for="name" class="form-label">Department Name</label>
                <input 
                  v-model="formData.name"
                  type="text" 
                  class="form-control"
                  id="name"
                  placeholder="Enter department name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea 
                  v-model="formData.description"
                  class="form-control"
                  id="description"
                  placeholder="Enter department description"
                  rows="5"
                  required
                ></textarea>
              </div>
              <button type="submit" class="btn btn-success w-100">Create</button>
            </form>
            <button @click="router.push('/admin_dashboard')" class="btn btn-secondary w-100 mt-3">Back</button>
          </div>
        </div>
      </div>
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
