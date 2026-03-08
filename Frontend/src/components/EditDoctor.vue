<template>
  <div class="container-fluid mt-5">
    <div class="card shadow">
      <div class="card-header bg-primary text-white">
        <h2 class="h4 mb-0">Edit Doctor</h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="submitEdit">
          <div class="mb-3">
            <label for="name" class="form-label">Fullname</label>
            <input v-model="formData.name" id="name" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Specialization/Department</label>
            <input :value="specializationName" class="form-control" disabled readonly />
          </div>

          <div class="mb-3">
            <label for="qualification" class="form-label">Qualification</label>
            <input v-model="formData.qualification" id="qualification" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label for="experience" class="form-label">Experience (years)</label>
            <input v-model.number="formData.experience" id="experience" type="number" min="0" class="form-control" required />
          </div>

          <div class="d-grid">
            <button type="submit" class="btn btn-primary">Update</button>
          </div>
        </form>
        <button @click="router.push('/admin_dashboard')" class="btn btn-secondary w-100 mt-3">Back</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter, useRoute } from 'vue-router'
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
