<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-12">
        <div class="card p-4">
          <h2 class="card-title text-center mb-4">Edit Department</h2>
          <form @submit.prevent="submitEdit">
            <div class="mb-3">
              <label for="name" class="form-label">Department Name</label>
              <input v-model="formData.name" id="name" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="description" class="form-label">Description</label>
              <textarea v-model="formData.description" id="description" rows="4" class="form-control" required></textarea>
            </div>

            <button type="submit" class="btn btn-primary w-100">Update</button>
          </form>
          <button @click="router.push('/admin_dashboard')" class="btn btn-secondary w-100 mt-3">Back</button>
        </div>
      </div>
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
