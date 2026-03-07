<template>
  <div>
    <AdminNavBar />
    <div class="container mt-4">
      <div v-if="searchResults">
        <div class="card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h2 class="h4 mb-0">Search Results</h2>
            <button @click="() => { searchResults = null; router.push('/admin_dashboard') }" class="btn btn-secondary">Clear</button>
          </div>
          <div class="card-body">
            <div v-if="(searchResults.doctors || []).length === 0 && (searchResults.patients || []).length === 0" class="alert alert-info">No results found</div>
            <div v-if="(searchResults.doctors || []).length > 0">
              <h3>Doctors</h3>
              <ul class="list-group mb-3">
                <li v-for="d in searchResults.doctors" :key="d.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <strong>Dr. {{ d.name }}</strong> - {{ d.specialization }}
                  </div>
                  <button @click="editDoctor(d.id)" class="btn btn-warning btn-sm">Edit</button>
                </li>
              </ul>
            </div>
            <div v-if="(searchResults.patients || []).length > 0">
              <h3>Patients</h3>
              <ul class="list-group">
                <li v-for="p in searchResults.patients" :key="p.id" class="list-group-item d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{{ p.name }}</strong> (Age: {{ p.age }})
                  </div>
                  <button @click="editPatient(p.id)" class="btn btn-warning btn-sm">Edit</button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div v-else>

        <div class="card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h2 class="h4 mb-0">Registered Doctors</h2>
            <button @click="goToAddDoctor" class="btn btn-success">+ Create</button>
          </div>
          <div class="card-body">
            <div v-if="doctors.length === 0" class="alert alert-info">No doctors found</div>
            <ul class="list-group">
              <li v-for="doctor in doctors" :key="doctor.id" class="list-group-item d-flex justify-content-between align-items-center">
                <strong>Dr. {{ doctor.name }}</strong>
                <div>
                  <button @click="editDoctor(doctor.id)" class="btn btn-warning btn-sm me-2">Edit</button>
                  <button @click="deleteDoctor(doctor.id)" class="btn btn-danger btn-sm me-2">Delete</button>
                  <button @click="blacklistDoctor(doctor.id)" class="btn btn-secondary btn-sm">Blacklist</button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div class="card mb-4">
          <div class="card-header">
            <h2 class="h4 mb-0">Registered Patients</h2>
          </div>
          <div class="card-body">
            <div v-if="patients.length === 0" class="alert alert-info">No patients found</div>
            <ul class="list-group">
              <li v-for="patient in patients" :key="patient.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ patient.name }}</strong> (Age: {{ patient.age }}, {{ patient.gender }})
                </div>
                <div>
                  <button @click="deletePatient(patient.id)" class="btn btn-danger btn-sm me-2">Delete</button>
                  <button @click="blacklistPatient(patient.id)" class="btn btn-secondary btn-sm me-2">Blacklist</button>
                  <button @click="goToPatientHistory(patient.id)" class="btn btn-primary btn-sm">View</button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div class="card mb-4">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h2 class="h4 mb-0">Departments</h2>
            <button @click="goToAddDepartment" class="btn btn-success">+ Add Department</button>
          </div>
          <div class="card-body">
            <div v-if="departments.length === 0" class="alert alert-info">No departments found</div>
            <ul class="list-group">
              <li v-for="department in departments" :key="department.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>{{ department.name }}</strong> - {{ department.description }}
                </div>
                <div>
                  <button @click="editDepartment(department.id)" class="btn btn-warning btn-sm me-2">Edit</button>
                  <button @click="deleteDepartment(department.id)" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h2 class="h4 mb-0">Upcoming Appointments</h2>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Sr No.</th>
                    <th>Patient Name</th>
                    <th>Doctor Name</th>
                    <th>Department</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="appointments.length === 0">
                    <td colspan="5" class="text-center text-muted">No appointments found</td>
                  </tr>
                  <tr v-for="(appointment, index) in appointments" :key="appointment.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ appointment.patient_name }}</td>
                    <td>{{ appointment.doctor_name }}</td>
                    <td>{{ appointment.department }}</td>
                    <td>{{ formatDate(appointment.appointment_date) }}</td>
                  </tr>
                </tbody>
              </table>
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
