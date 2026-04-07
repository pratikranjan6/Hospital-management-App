<template>
  <div class="admin-wrapper">
    <DoctorNavBar />
    
    <div class="admin-container">
      <!-- Patient Info Card -->
      <div class="info-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title"> Patient History</h2>
            <p class="card-subtitle">Medical visit records and history</p>
          </div>
        </div>
        <div class="card-body">
          <div class="patient-info">
            <div class="info-field">
              <span class="info-label">Patient Name:</span>
              <span class="info-value">{{ patientName }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Visit History Table Card -->
      <div class="history-card">
        <div class="card-header">
          <div class="header-content">
            <h3 class="card-title"> Visit History</h3>
            <p class="card-subtitle">{{ visits.length }} total visits</p>
          </div>
        </div>
        <div class="card-body">
          <div v-if="visits.length === 0" class="empty-state">
            <p>No visit history found</p>
          </div>
          
          <div v-else class="history-container">
            <div class="table-wrapper">
              <table class="history-table">
                <thead>
                  <tr>
                    <th class="col-visit">Visit</th>
                    <th class="col-doctor">Doctor</th>
                    <th class="col-dept">Department</th>
                    <th class="col-tests">Tests Done</th>
                    <th class="col-diagnosis">Diagnosis</th>
                    <th class="col-prescription">Prescription</th>
                    <th class="col-medicines">Medicines</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(visit, index) in visits" :key="visit.id" class="history-row">
                    <td class="col-visit">{{ index + 1 }}</td>
                    <td class="col-doctor">{{ visit.doctor_name || 'N/A' }}</td>
                    <td class="col-dept">{{ visit.department || 'N/A' }}</td>
                    <td class="col-tests">{{ visit.tests_done || 'None' }}</td>
                    <td class="col-diagnosis">{{ visit.diagnosis || 'Pending' }}</td>
                    <td class="col-prescription">{{ visit.prescription || 'None' }}</td>
                    <td class="col-medicines">
                      <div v-if="visit.medicines && visit.medicines.length > 0" class="medicines-list">
                        <span v-for="medicine in visit.medicines" :key="medicine" class="medicine-badge">
                          {{ medicine }}
                        </span>
                      </div>
                      <span v-else class="text-muted">None</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div class="button-group">
            <button @click="goBack" class="btn-back"> Back to Dashboard</button>
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
import DoctorNavBar from './DoctorNavBar.vue'
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.admin-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.admin-container {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

/* ========== INFO CARD ========== */
.info-card,
.history-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  animation: slideUp 0.5s ease-out;
  margin-bottom: 2rem;
}

.info-card {
  border-top: 4px solid #764ba2;
}

.history-card {
  border-top: 4px solid #3498db;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.history-card .card-header {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.card-subtitle {
  font-size: 0.9rem;
  opacity: 0.9;
  margin: 0.25rem 0 0;
}

.card-body {
  padding: 1.5rem;
}

/* ========== PATIENT INFO ========== */
.patient-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-field {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  /* border-left: 4px solid #764ba2; */
}

.info-label {
  font-weight: 600;
  color: #2c3e50;
  min-width: 150px;
}

.info-value {
  color: #667eea;
  font-weight: 500;
}

/* ========== HISTORY TABLE ========== */
.history-container {
  margin-bottom: 1.5rem;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 8px;
  border: 1px solid #e0e6ed;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.history-table thead {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  position: sticky;
  top: 0;
}

.history-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  min-width: 100px;
  white-space: nowrap;
}

.history-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e6ed;
  color: #2c3e50;
}

.history-table tbody tr {
  transition: all 0.3s ease;
}

.history-table tbody tr:hover {
  background: #f0f2f9;
}

.history-row:last-child td {
  border-bottom: none;
}

/* Column widths */
.col-visit,
.col-doctor {
  width: 100px;
}

.col-dept {
  width: 130px;
}

.col-tests,
.col-diagnosis,
.col-prescription {
  width: 120px;
}

.col-medicines {
  width: 150px;
}

/* ========== MEDICINES ========== */
.medicines-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.medicine-badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #7f8c8d;
  font-style: italic;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

/* ========== BUTTONS ========== */
.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  justify-content: center;
}

.btn-back {
  padding: 0.85rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-back:active {
  transform: translateY(0);
}

.text-muted {
  color: #7f8c8d;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1200px) {
  .col-visit,
  .col-doctor,
  .col-dept,
  .col-tests,
  .col-diagnosis,
  .col-prescription,
  .col-medicines {
    width: auto;
    min-width: 80px;
  }
}

@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    padding: 1.25rem;
  }

  .card-title {
    font-size: 1.3rem;
  }

  .card-subtitle {
    font-size: 0.8rem;
  }

  .card-body {
    padding: 1.25rem;
  }

  .history-table {
    font-size: 0.8rem;
  }

  .history-table th,
  .history-table td {
    padding: 0.75rem;
    min-width: 70px;
  }

  .info-field {
    flex-direction: column;
    gap: 0.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .btn-back {
    width: 100%;
    text-align: center;
  }

  .medicines-list {
    gap: 0.25rem;
  }

  .medicine-badge {
    padding: 0.3rem 0.6rem;
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .admin-container {
    padding: 0.75rem;
  }

  .card-header {
    padding: 1rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .history-table {
    font-size: 0.7rem;
  }

  .history-table th,
  .history-table td {
    padding: 0.5rem;
    min-width: 60px;
  }

  .info-label {
    min-width: 120px;
  }

  .btn-back {
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
