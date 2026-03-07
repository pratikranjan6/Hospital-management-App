<template>
  <div class="patient-history-container">
    <div class="patient-info">
      <h2>Patient History</h2>
      <div class="patient-details">
        <div class="detail-item">
          <span class="label">Patient Name:</span>
          <span class="value">{{ patientName }}</span>
        </div>
      </div>
    </div>

    <div class="visit-history">
      <h3>Visit History</h3>
      <div class="table-container">
        <table class="history-table">
          <thead>
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
              <td colspan="8" class="empty-message">No visit history found</td>
            </tr>
            <tr v-for="(visit, index) in visits" :key="visit.id">
              <td>{{ index + 1 }}</td>
              <td>{{ visit.doctor_name || 'N/A' }}</td>
              <td>{{ visit.department || 'N/A' }}</td>
              <td>{{ visit.tests_done }}</td>
              <td>{{ visit.diagnosis }}</td>
              <td>{{ visit.prescription }}</td>
              <td>
                <ul class="medicines-list">
                  <li v-for="medicine in visit.medicines" :key="medicine">
                    {{ medicine }}
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="goBack" class="btn-back">Back</button>
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
  router.push('/doctor_dashboard')
}
</script>

<style scoped>
/* reuse same styles as PatientHistory.vue */
.patient-history-container {
  padding: 40px;
  background: #f5f5f5;
  min-height: 100vh;
}

.patient-info {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.patient-info h2 {
  color: #333;
  margin-bottom: 20px;
  font-size: 22px;
}

.patient-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.detail-item .label {
  font-weight: 600;
  color: #555;
  font-size: 14px;
}

.detail-item .value {
  color: #333;
  font-size: 16px;
}

.visit-history {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.visit-history h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 18px;
}

.table-container {
  overflow-x: auto;
  margin-bottom: 20px;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.history-table thead {
  background: #f9f9f9;
  border-bottom: 2px solid #ddd;
}

.history-table th {
  padding: 15px;
  text-align: left;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.history-table td {
  padding: 15px;
  border-bottom: 1px solid #eee;
  color: #666;
  font-size: 14px;
}

.history-table tbody tr:hover {
  background: #f9f9f9;
}

.medicines-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.medicines-list li {
  margin-bottom: 4px;
}

.btn-back {
  padding: 10px 20px;
  background: #0f1724;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-back:hover {
  background: #1e293b;
}
</style>
