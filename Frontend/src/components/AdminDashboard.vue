<template>
  <div class="admin-wrapper">
    <AdminNavBar />
    
    <div class="admin-container">
      <!-- Search Results Section -->
      <div v-if="searchResults" class="search-results-section">
        <div class="section-header">
          <h2 class="section-title">🔍 Search Results</h2>
          <button @click="() => { searchResults = null; router.push('/admin_dashboard') }" class="btn-clear">
            ✕ Clear
          </button>
        </div>

        <div v-if="(searchResults.doctors || []).length === 0 && (searchResults.patients || []).length === 0" class="empty-state">
          <p>No results found for your search</p>
        </div>

        <div v-if="(searchResults.doctors || []).length > 0" class="search-card">
          <h3 class="card-title"> Doctors</h3>
          <div class="search-list">
            <div v-for="d in searchResults.doctors" :key="d.id" class="search-item">
              <div class="item-info">
                <strong>Dr. {{ d.name }}</strong>
                <span class="specialization">{{ d.specialization }}</span>
              </div>
              <button @click="editDoctor(d.id)" class="btn-action btn-edit">Edit</button>
            </div>
          </div>
        </div>

        <div v-if="(searchResults.patients || []).length > 0" class="search-card">
          <h3 class="card-title">👥 Patients</h3>
          <div class="search-list">
            <div v-for="p in searchResults.patients" :key="p.id" class="search-item">
              <div class="item-info">
                <strong>{{ p.name }}</strong>
                <span class="age-info">Age: {{ p.age }} years</span>
              </div>
              <button @click="editPatient(p.id)" class="btn-action btn-edit">Edit</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Section -->
      <div v-else class="dashboard-grid">
        <!-- Doctors Card -->
        <div class="dashboard-card doctors-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Registered Doctors</h3>
              <p class="card-subtitle">{{ doctors.length }} total doctors</p>
            </div>
            <button @click="goToAddDoctor" class="btn-primary">+ New Doctor</button>
          </div>
          <div class="card-body">
            <div v-if="doctors.length === 0" class="empty-state">No doctors registered yet</div>
            <div v-else class="items-list">
              <div v-for="doctor in doctors" :key="doctor.id" class="list-item doctor-item">
                <div class="item-content">
                  <h4>Dr. {{ doctor.name }}</h4>
                  <p class="specialty">{{ doctor.specialization }}</p>
                </div>
                <div class="item-actions">
                  <button @click="editDoctor(doctor.id)" class="btn-action btn-edit">Edit</button>
                  <button @click="deleteDoctor(doctor.id)" class="btn-action btn-delete">Delete</button>
                  <button @click="blacklistDoctor(doctor.id)" class="btn-action btn-block">Blacklist</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Patients Card -->
        <div class="dashboard-card patients-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Registered Patients</h3>
              <p class="card-subtitle">{{ patients.length }} total patients</p>
            </div>
          </div>
          <div class="card-body">
            <div v-if="patients.length === 0" class="empty-state">No patients registered yet</div>
            <div v-else class="items-list">
              <div v-for="patient in patients" :key="patient.id" class="list-item patient-item">
                <div class="item-content">
                  <h4>{{ patient.name }}</h4>
                  <p class="patient-info">Age: {{ patient.age }} • {{ patient.gender }}</p>
                </div>
                <div class="item-actions">
                  <button @click="goToPatientHistory(patient.id)" class="btn-action btn-view">View</button>
                  <button @click="deletePatient(patient.id)" class="btn-action btn-delete">Delete</button>
                  <button @click="blacklistPatient(patient.id)" class="btn-action btn-block">Blacklist</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Departments Card -->
        <div class="dashboard-card departments-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Departments</h3>
              <p class="card-subtitle">{{ departments.length }} departments</p>
            </div>
            <button @click="goToAddDepartment" class="btn-primary">+ New Dept</button>
          </div>
          <div class="card-body">
            <div v-if="departments.length === 0" class="empty-state">No departments found</div>
            <div v-else class="items-list">
              <div v-for="department in departments" :key="department.id" class="list-item dept-item">
                <div class="item-content">
                  <h4>{{ department.name }}</h4>
                  <p class="description">{{ department.description }}</p>
                </div>
                <div class="item-actions">
                  <button @click="editDepartment(department.id)" class="btn-action btn-edit">Edit</button>
                  <button @click="deleteDepartment(department.id)" class="btn-action btn-delete">Delete</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Appointments Card -->
        <div class="dashboard-card appointments-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Upcoming Appointments</h3>
              <p class="card-subtitle">{{ appointments.length }} appointments</p>
            </div>
          </div>
          <div class="card-body">
            <div v-if="appointments.length === 0" class="empty-state">No upcoming appointments</div>
            <div v-else class="appointments-table">
              <div class="table-header">
                <div class="col-patient">Patient</div>
                <div class="col-doctor">Doctor</div>
                <div class="col-dept">Department</div>
                <div class="col-date">Date & Time</div>
              </div>
              <div v-for="(appointment, index) in appointments" :key="appointment.id" class="table-row">
                <div class="col-patient">{{ appointment.patient_name }}</div>
                <div class="col-doctor">Dr. {{ appointment.doctor_name }}</div>
                <div class="col-dept">{{ appointment.department }}</div>
                <div class="col-date">{{ formatDate(appointment.appointment_date) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useRouter } from 'vue-router'
import AdminNavBar from './AdminNavBar.vue'
import { getApiBase, getAuthHeader } from '../utils/auth'

const router = useRouter()
const doctors = ref([])
const patients = ref([])
const appointments = ref([])
const departments = ref([])
const searchResults = ref(null)
const route = useRoute()

const API_BASE = getApiBase()

onMounted(async () => {
  const q = route.query.search
  if (q) {
    await performSearch(String(q))
  } else {
    await fetchDoctors()
    await fetchPatients()
    await fetchAppointments()
    await fetchDepartments()
  }
})

watch(() => route.query.search, async (newQ) => {
  if (newQ) await performSearch(String(newQ))
  else {
    searchResults.value = null
    await fetchDoctors()
    await fetchPatients()
    await fetchDepartments()
  }
})

async function performSearch(query) {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const resp = await axios.get(`${API_BASE}/api/admin/search`, {
      params: { q: query },
      headers: auth
    })
    searchResults.value = resp.data || { doctors: [], patients: [] }
  } catch (err) {
    console.error('Search failed:', err)
    alert('Search failed: ' + (err.response?.data?.msg || err.message))
  }
}

async function fetchDoctors() {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const response = await axios.get(`${API_BASE}/api/admin/doctors`, { headers: auth })
    doctors.value = response.data
  } catch (error) {
    console.error('Failed to fetch doctors:', error)
  }
}

async function fetchPatients() {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const response = await axios.get(`${API_BASE}/api/admin/patients`, { headers: auth })
    patients.value = response.data
  } catch (error) {
    console.error('Failed to fetch patients:', error)
  }
}

async function fetchAppointments() {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const response = await axios.get(`${API_BASE}/api/admin/appointments`, { headers: auth })
    appointments.value = response.data
  } catch (error) {
    console.error('Failed to fetch appointments:', error)
  }
}

async function fetchDepartments() {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    const response = await axios.get(`${API_BASE}/api/departments`, { headers: auth })
    departments.value = response.data
  } catch (error) {
    console.error('Failed to fetch departments:', error)
  }
}

function goToAddDoctor() {
  router.push('/add_doctor')
}
function editDoctor(doctorId) {
  router.push(`/edit_doctor/${doctorId}`)
}

function goToPatientHistory(patientId) {
  router.push({
    path: '/patient_history',
    query: { patient_id: patientId }
  })
}

function goToAddDepartment() {
  router.push('/add_department')
}

async function deleteDoctor(doctorId) {
  if (!confirm('Are you sure you want to delete this doctor?')) return
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    await axios.delete(`${API_BASE}/api/admin/doctor/${doctorId}`, { headers: auth })
    doctors.value = doctors.value.filter(d => d.id !== doctorId)
  } catch (err) {
    console.error('Failed to delete doctor:', err)
    alert('Failed to delete doctor')
  }
}

async function deletePatient(patientId) {
  if (!confirm('Are you sure you want to delete this patient?')) return
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    await axios.delete(`${API_BASE}/api/admin/patient/${patientId}`, { headers: auth })
    patients.value = patients.value.filter(p => p.id !== patientId)
  } catch (err) {
    console.error('Failed to delete patient:', err)
    alert('Failed to delete patient')
  }
}

async function deleteDepartment(departmentId) {
  if (!confirm('Are you sure you want to delete this department?')) return
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    await axios.delete(`${API_BASE}/api/admin/department/${departmentId}`, { headers: auth })
    departments.value = departments.value.filter(d => d.id !== departmentId)
  } catch (err) {
    console.error('Failed to delete department:', err)
    const serverMsg = err.response?.data?.msg || err.response?.data?.message
    if (serverMsg) {
      alert('Failed to delete department: ' + serverMsg)
    } else {
      alert('Failed to delete department (network/server error)')
    }
  }
}

function editDepartment(departmentId) {
  router.push(`/edit_department/${departmentId}`)
}

async function blacklistPatient(patientId) {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    await axios.post(`${API_BASE}/api/admin/patient/${patientId}/blacklist`, {}, { headers: auth })
    alert('Patient blacklisted successfully')
    await fetchPatients()
  } catch (err) {
    console.error('Failed to blacklist patient:', err)
    alert('Failed to blacklist patient')
  }
}

async function blacklistDoctor(doctorId) {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    await axios.post(`${API_BASE}/api/admin/doctor/${doctorId}/blacklist`, {}, { headers: auth })
    alert('Doctor blacklisted successfully')
    await fetchDoctors()
  } catch (err) {
    console.error('Failed to blacklist doctor:', err)
    alert('Failed to blacklist doctor')
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
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
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* ========== SEARCH RESULTS ========== */
.search-results-section {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
}

.btn-clear {
  padding: 0.75rem 1.5rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-clear:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

.search-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.search-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  /* border-left: 4px solid #667eea; */
  transition: all 0.3s ease;
}

.search-item:hover {
  background: #f0f2f9;
  transform: translateX(5px);
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.specialization,
.age-info {
  font-size: 0.85rem;
  color: #666;
}

/* ========== DASHBOARD GRID ========== */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
  gap: 2rem;
  animation: slideUp 0.5s ease-out;
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

/* ========== CARDS ========== */
.dashboard-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  /* border-top: 4px solid #667eea; */
  animation: cardSlide 0.5s ease-out;
}

@keyframes cardSlide {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dashboard-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  transform: translateY(-5px);
}

.doctors-card {
  border-top-color: #667eea;
}

.patients-card {
  border-top-color: #764ba2;
}

.departments-card {
  border-top-color: #f093fb;
}

.appointments-card {
  border-top-color: #1dd1a1;
  grid-column: 1 / -1;
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.card-body {
  padding: 1.5rem;
}

/* ========== BUTTONS ========== */
.btn-primary {
  padding: 0.75rem 1.25rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 0.9rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-action {
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
  background: transparent;
  border: 1px solid #ddd;
}

.btn-action:hover {
  transform: scale(1.1);
}

.btn-edit {
  color: #f39c12;
}

.btn-edit:hover {
  background: #fff3e0;
  border-color: #f39c12;
}

.btn-delete {
  color: #e74c3c;
}

.btn-delete:hover {
  background: #ffe0e0;
  border-color: #e74c3c;
}

.btn-block {
  color: #9b59b6;
}

.btn-block:hover {
  background: #f4ecf7;
  border-color: #9b59b6;
}

.btn-view {
  color: #3498db;
}

.btn-view:hover {
  background: #e0f2f9;
  border-color: #3498db;
}

/* ========== LISTS ========== */
.items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  /* border-left: 3px solid #667eea; */
  transition: all 0.2s ease;
}

.list-item:hover {
  background: #f0f2f9;
  transform: translateX(5px);
}

.patient-item {
  border-left-color: #764ba2;
}

.dept-item {
  border-left-color: #f093fb;
}

.item-content h4 {
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.specialty,
.patient-info,
.description {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

/* ========== APPOINTMENTS TABLE ========== */
.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1fr 1.5fr;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  position: sticky;
  top: 0;
}

.table-row {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1fr 1.5fr;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  /* border-left: 3px solid #1dd1a1; */
  transition: all 0.2s ease;
}

.table-row:hover {
  background: #f0f2f9;
  transform: translateX(5px);
}

.col-patient,
.col-doctor,
.col-dept,
.col-date {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  color: #2c3e50;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
  font-style: italic;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  }

  .appointments-card {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .btn-primary {
    width: 100%;
    text-align: center;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .table-header div::before,
  .table-row div::before {
    content: attr(data-label);
    font-weight: 600;
    color: #667eea;
  }

  .search-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .item-actions {
    width: 100%;
    justify-content: space-between;
  }
}

@media (max-width: 480px) {
  .admin-container {
    padding: 0.75rem;
  }

  .section-title {
    font-size: 1.2rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .item-content h4 {
    font-size: 0.95rem;
  }

  .btn-action {
    padding: 0.4rem 0.6rem;
    font-size: 0.9rem;
  }
}
</style>
