<template>
  <div class="edit-department-container">
    <div class="form-section">
      <h2>Edit Department</h2>
      <form @submit.prevent="submitEdit" class="department-form">
        <div class="form-group">
          <label for="name">Department Name</label>
          <input v-model="formData.name" id="name" type="text" required />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea v-model="formData.description" id="description" rows="4" required></textarea>
        </div>

        <button type="submit" class="btn-create">Update</button>
      </form>
      <button @click="router.push('/admin_dashboard')" class="btn btn-secondary w-100 mt-3">Back</button> 
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
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
.edit-department-container { padding: 40px; min-height: 100vh; background: #f5f5f5 }
.form-section { max-width: 600px; margin: 0 auto; background: #fff; padding: 36px; border-radius: 8px }
.form-section h2 { text-align:center; margin-bottom: 20px }
.department-form { display:flex; flex-direction:column; gap:16px }
.form-group { display:flex; flex-direction:column; gap:8px }
.form-group input, .form-group textarea { padding:10px; border:1px solid #ddd; border-radius:4px }
.btn-create { padding:12px; background:#1976d2; color:white; border:none; border-radius:6px; cursor:pointer }
.btn-create:hover { background:#165fa8 }
</style>
