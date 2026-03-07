<template>
  <div class="edit-doctor-container">
    <div class="form-section">
      <h2>Edit Doctor</h2>
      <form @submit.prevent="submitEdit" class="doctor-form">

        <div class="form-group">
          <label for="name">Fullname</label>
          <input v-model="formData.name" id="name" type="text" required />
        </div>

        <div class="form-group">
          <label>Specialization/Department</label>
          <input :value="specializationName" disabled />
        </div>

        <div class="form-group">
          <label for="qualification">Qualification</label>
          <input v-model="formData.qualification" id="qualification" type="text" required />
        </div>

        <div class="form-group">
          <label for="experience">Experience (years)</label>
          <input v-model.number="formData.experience" id="experience" type="number" min="0" required />
        </div>

        <div class="form-group">
          <label for="availability">Availability</label>
          <input v-model="formData.availability" id="availability" type="text" required />
        </div>

        <button type="submit" class="btn-update">Update</button>
      </form>
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
  experience: 0,
  availability: ''
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
    formData.value.availability = doc.availability || ''
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
        experience: formData.value.experience,
        availability: formData.value.availability
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
.edit-doctor-container { padding: 40px; min-height: 100vh; background: #f5f5f5 }
.form-section { max-width: 600px; margin: 0 auto; background: #fff; padding: 36px; border-radius: 8px }
.form-section h2 { text-align:center;color:black; margin-bottom: 20px }
.doctor-form { display:flex; flex-direction:column; gap:16px }
.form-group { display:flex; color:black;flex-direction:column; gap:8px }
.form-group input { padding:10px; border:1px solid #ddd;background-color: #ddd;color:black; border-radius:4px }
.btn-update { padding:12px; background:#1976d2; color:white; border:none; border-radius:6px; cursor:pointer }
.btn-update:hover { background:#165fa8 }
</style>
