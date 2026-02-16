<template>
  <div class="admin-welcome-container">
    <div class="welcome-content">
      <div class="welcome-header">
        <h1>Welcome to Hospital Management System</h1>
        <p class="subtitle">Admin Dashboard</p>
      </div>

      <div class="welcome-card">
        <h2>Overview</h2>
        <p>Welcome to the Hospital Management System Admin Panel. From here you can manage:</p>
        <ul class="feature-list">
          <li>
            <strong>Doctors:</strong> Add, edit, view, and manage doctor information, specializations, and availability.
          </li>
          <li>
            <strong>Patients:</strong> Track patient information, medical history, and appointments.
          </li>
          <li>
            <strong>Departments:</strong> Create and manage hospital departments.
          </li>
          <li>
            <strong>Appointments:</strong> View and manage all scheduled appointments.
          </li>
        </ul>
      </div>

      <div class="stats-container">
        <div class="stat-card">
          <div class="stat-icon doctors-icon">👨‍⚕️</div>
          <div class="stat-content">
            <h3>Total Doctors</h3>
            <p class="stat-number">{{ doctorCount }}</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon patients-icon">👥</div>
          <div class="stat-content">
            <h3>Total Patients</h3>
            <p class="stat-number">{{ patientCount }}</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon departments-icon">🏥</div>
          <div class="stat-content">
            <h3>Departments</h3>
            <p class="stat-number">{{ departmentCount }}</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon appointments-icon">📅</div>
          <div class="stat-content">
            <h3>Appointments</h3>
            <p class="stat-number">{{ appointmentCount }}</p>
          </div>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="goToAddDoctor" class="btn btn-primary">+ Add Doctor</button>
        <button @click="goToAddDepartment" class="btn btn-primary">+ Add Department</button>
        <button @click="goToDashboard" class="btn btn-secondary">Go to Dashboard</button>
      </div>

      <div class="info-card">
        <h3>Quick Tips</h3>
        <ul>
          <li>Use the search bar in the navbar to quickly find doctors, patients, or departments.</li>
          <li>Click on the "View" button next to a patient to see their medical history.</li>
          <li>You can edit, delete, or blacklist any doctor or patient from the dashboard.</li>
          <li>All appointments are listed in the Upcoming Appointments section on the dashboard.</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { getApiBase } from '../utils/auth'

const router = useRouter()
const API_BASE = getApiBase()

const doctorCount = ref(0)
const patientCount = ref(0)
const departmentCount = ref(0)
const appointmentCount = ref(0)

onMounted(async () => {
  await fetchStats()
})

async function fetchStats() {
  try {
    const token = localStorage.getItem('token')
    
    const [doctorsRes, patientsRes, deptsRes, appointsRes] = await Promise.all([
      axios.get(`${API_BASE}/api/admin/doctors`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${API_BASE}/api/admin/patients`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${API_BASE}/api/departments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      axios.get(`${API_BASE}/api/admin/appointments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
    ])

    doctorCount.value = doctorsRes.data.length || 0
    patientCount.value = patientsRes.data.length || 0
    departmentCount.value = deptsRes.data.length || 0
    appointmentCount.value = appointsRes.data.length || 0
  } catch (error) {
    console.error('Failed to fetch statistics:', error)
  }
}

function goToAddDoctor() {
  router.push('/add_doctor')
}

function goToAddDepartment() {
  router.push('/add_department')
}

function goToDashboard() {
  router.push('/admin_dashboard')
}
</script>

<style scoped>
.admin-welcome-container {
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
}

.welcome-content {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-header {
  text-align: center;
  margin-bottom: 3rem;
  color: #2c3e50;
}

.welcome-header h1 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.welcome-header .subtitle {
  font-size: 1.2rem;
  color: #7f8c8d;
}

.welcome-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.welcome-card h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.welcome-card p {
  color: #555;
  margin-bottom: 1.5rem;
  font-size: 1rem;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 0.8rem 0;
  color: #555;
  border-bottom: 1px solid #eee;
}

.feature-list li:last-child {
  border-bottom: none;
}

.feature-list strong {
  color: #2c3e50;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.stat-icon {
  font-size: 2.5rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #f0f0f0;
}

.doctors-icon {
  background: #e8f5e9;
}

.patients-icon {
  background: #e3f2fd;
}

.departments-icon {
  background: #fff3e0;
}

.appointments-icon {
  background: #f3e5f5;
}

.stat-content h3 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.stat-number {
  color: #4CAF50;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 2rem;
}

.btn {
  padding: 0.8rem 1.8rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
}

.btn-secondary {
  background: #3b82f6;
  color: white;
}

.btn-secondary:hover {
  background: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.info-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-top: 2rem;
}

.info-card h3 {
  color: #2c3e50;
  margin-top: 0;
  font-size: 1.5rem;
}

.info-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-card li {
  padding: 0.8rem 0;
  color: #555;
  border-left: 4px solid #4CAF50;
  padding-left: 1rem;
}

@media (max-width: 768px) {
  .welcome-header h1 {
    font-size: 2rem;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
