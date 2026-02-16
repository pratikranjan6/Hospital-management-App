<template>
  <div>
    <AdminNavBar />
    <div class="admin-container">
      <div v-if="searchResults">
        <div class="search-results">
          <div class="section">
            <div class="section-header">
              <h2>Search Results</h2>
              <button @click="() => { searchResults = null; router.push('/admin_dashboard') }" class="btn btn-create">Clear</button>
            </div>
            <div class="section-content">
              <div v-if="(searchResults.doctors || []).length === 0 && (searchResults.patients || []).length === 0" class="empty-message">No results found</div>
              <div v-if="(searchResults.doctors || []).length > 0">
                <h3>Doctors</h3>
                <div v-for="d in searchResults.doctors" :key="d.id" class="item-row">
                  <span class="item-name">Dr. {{ d.name }}</span>
                  <span class="item-info">{{ d.specialization }}</span>
                  <div class="actions">
                    <button @click="editDoctor(d.id)" class="btn-edit">Edit</button>
                  </div>
                </div>
              </div>
              <div v-if="(searchResults.patients || []).length > 0">
                <h3>Patients</h3>
                <div v-for="p in searchResults.patients" :key="p.id" class="item-row">
                  <span class="item-name">{{ p.name }}</span>
                  <span class="item-info">(Age: {{ p.age }})</span>
                  <div class="actions">
                    <button @click="editPatient(p.id)" class="btn-edit">Edit</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <!-- Registered Doctors Section -->
        <div class="section">
          <div class="section-header">
            <h2>Registered Doctors</h2>
            <button @click="goToAddDoctor" class="btn btn-create">+ Create</button>
          </div>
          <div class="section-content">
            <div v-if="doctors.length === 0" class="empty-message">No doctors found</div>
            <div v-for="doctor in doctors" :key="doctor.id" class="item-row">
              <span class="item-name">Dr. {{ doctor.name }}</span>
              <div class="actions">
                <button @click="editDoctor(doctor.id)" class="btn-edit">Edit</button>
                <button @click="deleteDoctor(doctor.id)" class="btn-delete">Delete</button>
                <button @click="blacklistDoctor(doctor.id)" class="btn-blacklist">Blacklist</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Registered Patients Section -->
        <div class="section">
          <div class="section-header">
            <h2>Registered Patients</h2>
          </div>
          <div class="section-content">
            <div v-if="patients.length === 0" class="empty-message">No patients found</div>
            <div v-for="patient in patients" :key="patient.id" class="item-row">
              <span class="item-name">{{ patient.name }}</span>
              <span class="item-info">(Age: {{ patient.age }}, {{ patient.gender }})</span>
              <div class="actions">
                <button @click="editPatient(patient.id)" class="btn-edit">Edit</button>
                <button @click="deletePatient(patient.id)" class="btn-delete">Delete</button>
                <button @click="blacklistPatient(patient.id)" class="btn-blacklist">Blacklist</button>
                <button @click="goToPatientHistory(patient.id)" class="btn-view">View</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Departments Section -->
        <div class="section">
          <div class="section-header">
            <h2>Departments</h2>
            <button @click="goToAddDepartment" class="btn btn-create">+ Add Department</button>
          </div>
          <div class="section-content">
            <div v-if="departments.length === 0" class="empty-message">No departments found</div>
            <div v-for="department in departments" :key="department.id" class="item-row">
              <span class="item-name">{{ department.name }}</span>
              <span class="item-info">{{ department.description }}</span>
              <div class="actions">
                <button @click="editDepartment(department.id)" class="btn-edit">Edit</button>
                <button @click="deleteDepartment(department.id)" class="btn-delete">Delete</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Upcoming Appointments Section -->
        <div class="section">
          <h2>Upcoming Appointments</h2>
          <div class="table-container">
            <table class="appointments-table">
              <thead>
                <tr>
                  <th>Sr No.</th>
                  <th>Patient Name</th>
                  <th>Doctor Name</th>
                  <th>Department</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="appointments.length === 0">
                  <td colspan="7" class="empty-message">No appointments found</td>
                </tr>
                <tr v-for="(appointment, index) in appointments" :key="appointment.id">
                  <td>{{ index + 1 }}</td>
                  <td>{{ appointment.patient_name }}</td>
                  <td>{{ appointment.doctor_name }}</td>
                  <td>{{ appointment.department }}</td>
                  <td>{{ formatDate(appointment.appointment_date) }}</td>
                  <td>
                    <span class="status" :class="appointment.status.toLowerCase()">
                      {{ appointment.status }}
                    </span>
                  </td>
                  <td>
                    <button class="btn-view">View</button>
                  </td>
                </tr>
              </tbody>
            </table>
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
    console.debug('Searching with headers:', auth, 'q=', query)
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
    console.debug('Fetching doctors with headers:', auth)
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
    console.debug('Fetching patients with headers:', auth)
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
    console.debug('Fetching appointments with headers:', auth)
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
    console.debug('Fetching departments with headers:', auth)
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
  if (!confirm('Delete this doctor?')) return
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    console.debug('Deleting doctor with headers:', auth)
    await axios.delete(`${API_BASE}/api/admin/doctor/${doctorId}`, { headers: auth })
    doctors.value = doctors.value.filter(d => d.id !== doctorId)
  } catch (err) {
    console.error('Failed to delete doctor:', err)
    alert('Failed to delete doctor')
  }
}

async function deletePatient(patientId) {
  if (!confirm('Delete this patient?')) return
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    console.debug('Deleting patient with headers:', auth)
    await axios.delete(`${API_BASE}/api/admin/patient/${patientId}`, { headers: auth })
    patients.value = patients.value.filter(p => p.id !== patientId)
  } catch (err) {
    console.error('Failed to delete patient:', err)
    alert('Failed to delete patient')
  }
}

async function deleteDepartment(departmentId) {
  if (!confirm('Delete this department?')) return
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    console.debug('Deleting department with headers:', auth)
    const res = await axios.delete(`${API_BASE}/api/admin/department/${departmentId}`, { headers: auth })
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

function editPatient(patientId) {
  router.push(`/edit_patient/${patientId}`)
}

function editDepartment(departmentId) {
  router.push(`/edit_department/${departmentId}`)
}

async function blacklistPatient(patientId) {
  try {
    const auth = getAuthHeader()
    if (!auth.Authorization) { router.push('/login'); return }
    console.debug('Blacklisting patient with headers:', auth)
    await axios.post(`${API_BASE}/api/admin/patient/${patientId}/blacklist`, {}, { headers: auth })
    alert('Patient blacklisted')
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
    console.debug('Blacklisting doctor with headers:', auth)
    await axios.post(`${API_BASE}/api/admin/doctor/${doctorId}/blacklist`, {}, { headers: auth })
    alert('Doctor blacklisted')
    await fetchDoctors()
  } catch (err) {
    console.error('Failed to blacklist doctor:', err)
    alert('Failed to blacklist doctor')
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 2rem;
}

/* Sections */
.section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 1rem;
}

.section-header h2 {
  color: #324e6a;
  font-size: 1.3rem;
}

.btn-create {
  background-color: #48bb78;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.btn-create:hover {
  background-color: #38a169;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 6px;
  border-left: 4px solid #3b82f6;
}

.item-name {
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
}

.item-info {
  color: #718096;
  margin-right: 1rem;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete,
.btn-blacklist,
.btn-view {
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-edit {
  background-color: #ffd700;
  color: #333;
}

.btn-edit:hover {
  background-color: #ffed4e;
}

.btn-delete {
  background-color: #ef4444;
  color: white;
}

.btn-delete:hover {
  background-color: #dc2626;
}

.btn-blacklist {
  background-color: #6b7280;
  color: white;
}

.btn-blacklist:hover {
  background-color: #4b5563;
}

.btn-view {
  background-color: #3b82f6;
  color: white;
}

.btn-view:hover {
  background-color: #2563eb;
}

/* Table */
.table-container {
  overflow-x: auto;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.appointments-table thead {
  background-color: #f8f9fa;
}

.appointments-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
}

.appointments-table td {
  padding: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.appointments-table tbody tr:hover {
  background-color: #f8f9fa;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status.pending {
  background-color: #fef3c7;
  color: #92400e;
}

.status.confirmed {
  background-color: #dbeafe;
  color: #1e40af;
}

.status.completed {
  background-color: #dcfce7;
  color: #166534;
}

.status.cancelled {
  background-color: #fee2e2;
  color: #991b1b;
}

.empty-message {
  text-align: center;
  color: #718096;
  padding: 2rem;
  font-style: italic;
}

.btn {
  transition: all 0.3s ease;
}
</style>
