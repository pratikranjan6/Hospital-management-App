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
              <div v-for="(doctor, index) in doctors" v-show="expandedDoctors || index < ITEMS_PER_PAGE" :key="doctor.id" class="list-item doctor-item">
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
              <button v-if="doctors.length > ITEMS_PER_PAGE" @click="toggleDoctors" class="btn-show-more">
                {{ expandedDoctors ? '▼ Show Less' : '▶ Show More' }}
              </button>
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
              <div v-for="(patient, index) in patients" v-show="expandedPatients || index < ITEMS_PER_PAGE" :key="patient.id" class="list-item patient-item">
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
              <button v-if="patients.length > ITEMS_PER_PAGE" @click="togglePatients" class="btn-show-more">
                {{ expandedPatients ? '▼ Show Less' : '▶ Show More' }}
              </button>
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
              <div v-for="(department, index) in departments" v-show="expandedDepartments || index < ITEMS_PER_PAGE" :key="department.id" class="list-item dept-item">
                <div class="item-content">
                  <h4>{{ department.name }}</h4>
                  <p class="description">{{ department.description }}</p>
                </div>
                <div class="item-actions">
                  <button @click="editDepartment(department.id)" class="btn-action btn-edit">Edit</button>
                  <button @click="deleteDepartment(department.id)" class="btn-action btn-delete">Delete</button>
                </div>
              </div>
              <button v-if="departments.length > ITEMS_PER_PAGE" @click="toggleDepartments" class="btn-show-more">
                {{ expandedDepartments ? '▼ Show Less' : '▶ Show More' }}
              </button>
            </div>
          </div>
        </div>

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
              <div v-for="(appointment, index) in appointments" v-show="expandedAppointments || index < ITEMS_PER_PAGE" :key="appointment.id" class="table-row">
                <div class="col-patient">{{ appointment.patient_name }}</div>
                <div class="col-doctor">Dr. {{ appointment.doctor_name }}</div>
                <div class="col-dept">{{ appointment.department }}</div>
                <div class="col-date">{{ formatDate(appointment.appointment_date) }}</div>
              </div>
              <button v-if="appointments.length > ITEMS_PER_PAGE" @click="toggleAppointments" class="btn-show-more btn-show-more-appointments">
                {{ expandedAppointments ? ' Show Less' : ' Show More' }}
              </button>
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

const expandedDoctors = ref(false)
const expandedPatients = ref(false)
const expandedDepartments = ref(false)
const expandedAppointments = ref(false)

const ITEMS_PER_PAGE = 5

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

function toggleDoctors() {
  expandedDoctors.value = !expandedDoctors.value
}

function togglePatients() {
  expandedPatients.value = !expandedPatients.value
}

function toggleDepartments() {
  expandedDepartments.value = !expandedDepartments.value
}

function toggleAppointments() {
  expandedAppointments.value = !expandedAppointments.value
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
  background: #f2e8d8;
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
  font-weight: 800;
  color: #3d362f;
  letter-spacing: -0.02em;
}

.btn-clear {
  padding: 0.75rem 1.5rem;
  background: #8f7b65;
  color: white;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s ease;
}

.btn-clear:hover {
  background: #7a6a58;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(143, 123, 101, 0.3);
}

.search-card {
  background: #fffdf7;
  border-radius: 24px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
  border: 1px solid #d8c8b0;
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
  background: #fff9f1;
  border-radius: 16px;
  /* border-left: 4px solid #8f7b65; */
  transition: all 0.3s ease;
}

.search-item:hover {
  background: #f7eee5;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.1);
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.specialization,
.age-info {
  font-size: 0.85rem;
  color: #7d6d5f;
}

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

.dashboard-card {
  background: #fffdf7;
  border-radius: 24px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: all 0.3s ease;
  /* border-top: 4px solid #8f7b65; */
  border: 1px solid #d8c8b0;
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

.doctors-card {
  border-top-color: #8f7b65;
}

.patients-card {
  border-top-color: #a68a72;
}

.departments-card {
  border-top-color: #b59881;
}

.appointments-card {
  border-top-color: #8f7b65;
  grid-column: 1 / -1;
}

.card-header {
  padding: 1.5rem;
  background: #f4e9db;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid #dacbb8;
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #3d362f;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #7d6d5f;
}

.card-body {
  padding: 1.5rem;
}

/* ========== BUTTONS ========== */
.btn-primary {
  padding: 0.75rem 1.25rem;
  background: #8f7b65;
  color: white;
  border: none;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 0.9rem;
}

.btn-primary:hover {
  transform: translateY(-2px);
  background: #7a6a58;
  box-shadow: 0 8px 20px rgba(143, 123, 101, 0.3);
}

.btn-action {
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
  background: transparent;
  border: 1px solid #d8c8b0;
  font-weight: 600;
}

.btn-action:hover {
  transform: scale(1.1);
}

.btn-edit {
  color: #8f7b65;
}

.btn-edit:hover {
  background: #f0e5d8;
  border-color: #8f7b65;
}

.btn-delete {
  color: #c85a5a;
}

.btn-delete:hover {
  background: #f5dede;
  border-color: #c85a5a;
}

.btn-block {
  color: #a68a72;
}

.btn-block:hover {
  background: #f0e5d8;
  border-color: #a68a72;
}

.btn-view {
  color: #8f7b65;
}

.btn-view:hover {
  background: #f7eee5;
  border-color: #8f7b65;
}

.btn-show-more {
  width: 100%;
  padding: 0.75rem 1.25rem;
  margin-top: 1rem;
  background: #f4e9db;
  color: #3d362f;
  border: 2px solid #d8c8b0;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-show-more:hover {
  background: #e8dcc8;
  border-color: #8f7b65;
  color: #8f7b65;
}

.btn-show-more-appointments {
  margin-top: 0.75rem;
}

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
  background: #fff9f1;
  border-radius: 16px;
  /* border-left: 3px solid #8f7b65; */
  transition: all 0.2s ease;
}

.list-item:hover {
  background: #f7eee5;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.1);
}

.patient-item {
  border-left-color: #a68a72;
}

.dept-item {
  border-left-color: #b59881;
}

.item-content h4 {
  color: #3d362f;
  font-size: 1rem;
  margin-bottom: 0.25rem;
  font-weight: 700;
}

.specialty,
.patient-info,
.description {
  font-size: 0.85rem;
  color: #7d6d5f;
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
  background: #f4e9db;
  color: #3d362f;
  font-weight: 700;
  border-radius: 16px;
  margin-bottom: 0.5rem;
  position: sticky;
  top: 0;
  border: 1px solid #dacbb8;
}

.table-row {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1fr 1.5fr;
  gap: 1rem;
  padding: 1rem;
  background: #fff9f1;
  border-radius: 16px;
  margin-bottom: 0.5rem;
  /* border-left: 3px solid #8f7b65; */
  transition: all 0.2s ease;
}

.table-row:hover {
  background: #f7eee5;
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.1);
}

.col-patient,
.col-doctor,
.col-dept,
.col-date {
  display: flex;
  align-items: center;
  font-size: 0.95rem;
  color: #3d362f;
  font-weight: 500;
}

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6d5f53;
  font-style: italic;
  background: #fff9f1;
  border-radius: 16px;
  border: 2px dashed #d7c7b5;
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
