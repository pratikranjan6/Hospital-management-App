<template>
  <div class="container-fluid bg-light min-vh-100 py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow mb-4">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Patient History</h2>
            <div class="row">
              <div class="col-md-6">
                <div class="mb-3">
                  <strong>Patient Name:</strong> {{ patientName }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card shadow">
          <div class="card-body">
            <h3 class="card-title mb-4">Visit History</h3>
            <div class="table-responsive">
              <table class="table table-striped table-hover">
                <thead class="table-dark">
                  <tr>
                    <th>Visit No.</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Tests Done</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Medicines</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="visits.length === 0">
                    <td colspan="7" class="text-center text-muted py-5">No visit history found</td>
                  </tr>
                  <tr v-for="(visit, index) in visits" :key="visit.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ visit.doctor_name || 'N/A' }}</td>
                    <td>{{ visit.department || 'N/A' }}</td>
                    <td>{{ visit.tests_done }}</td>
                    <td>{{ visit.diagnosis }}</td>
                    <td>{{ visit.prescription }}</td>
                    <td>
                      <ul class="list-unstyled">
                        <li v-for="medicine in visit.medicines" :key="medicine" class="mb-1">
                          <i class="bi bi-check-circle-fill text-success me-2"></i>{{ medicine }}
                        </li>
                      </ul>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="text-center mt-4">
              <button @click="goBack" class="btn btn-success">Back</button>
            </div>
          </div>
        </div>
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

const patientName = ref('')
const visits = ref([])

onMounted(async () => {
  const patientId = route.query.patient_id
  
  if (patientId) {
    await fetchPatientHistory(patientId)
  }
})

async function fetchPatientHistory(patientId) {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_BASE}/api/patient/${patientId}/history`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    
    const data = response.data
    patientName.value = data.patient_name || 'N/A'
    visits.value = data.appointments || []
  } catch (error) {
    console.error('Failed to fetch patient history:', error)
    alert('Error loading patient history: ' + (error.response?.data?.msg || error.message))
  }
}

function goBack() {
  router.push('/admin_dashboard')
}
</script>
