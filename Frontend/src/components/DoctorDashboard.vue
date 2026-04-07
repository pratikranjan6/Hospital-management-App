<template>
  <div class="doctor-wrapper">
    <DoctorNavBar />

    <div class="doctor-container">
      <!-- Welcome Header -->
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title"> Welcome, Dr. {{ doctorName }}</h1>
          <p class="welcome-subtitle">Manage your appointments and patient care</p>
        </div>
      </div>

      <!-- Dashboard Grid -->
      <div class="dashboard-grid">
        <!-- Appointments Card -->
        <div class="dashboard-card appointments-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Upcoming Appointments</h3>
              <p class="card-subtitle">{{ appointments.length }} appointments</p>
            </div>
          </div>
          <div class="card-body">
            <div v-if="appointments.length === 0" class="empty-state">
              <p>No upcoming appointments scheduled</p>
            </div>
            <div v-else class="appointments-list">
              <div v-for="(appointment, index) in appointments" :key="appointment.id" class="appointment-item">
                <div class="appointment-number">{{ index + 1 }}</div>
                <div class="appointment-info">
                  <h4>{{ appointment.patient_name }}</h4>
                  <p class="appointment-time">Status: <span class="status-badge">{{ appointment.status }}</span></p>
                </div>
                <div class="appointment-actions">
                  <button @click="updateHistory(appointment.id)" class="btn-action btn-update" title="Update">Update</button>
                  <button @click="markComplete(appointment.id)" class="btn-action btn-complete" title="Complete">Complete</button>
                  <button @click="cancelAppointment(appointment.id)" class="btn-action btn-cancel" title="Cancel">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Patients Card -->
        <div class="dashboard-card patients-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Assigned Patients</h3>
              <p class="card-subtitle">{{ patients.length }} patients</p>
            </div>
          </div>
          <div class="card-body">
            <div v-if="patients.length === 0" class="empty-state">
              <p>No patients assigned yet</p>
            </div>
            <div v-else class="patients-list">
              <div v-for="patient in patients" :key="patient.id" class="patient-item">
                <div class="patient-avatar"></div>
                <div class="patient-info">
                  <h4>{{ patient.name }}</h4>
                  <p class="patient-id">ID: {{ patient.id }}</p>
                </div>
                <button @click="viewPatient(patient.id)" class="btn-action btn-view">View</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Availability Card -->
        <div class="dashboard-card availability-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Availability</h3>
              <p class="card-subtitle">Manage your schedule</p>
            </div>
          </div>
          <div class="card-body">
            <div class="availability-content">
              <p class="availability-desc">Set your availability for appointments</p>
              <button @click="provideAvailability" class="btn-primary">Set Availability</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DoctorNavBar from './DoctorNavBar.vue'
import { getApiBase, getAuthHeader } from '../utils/auth.js'

export default {
  name: 'DoctorDashboard',
  components: { DoctorNavBar },
  data() {
    return {
      doctorName: 'Doctor',
      appointments: [],
      patients: []
    }
  },
  methods: {
    fetchData() {
      const username = localStorage.getItem('username')
      const q = username ? `?username=${encodeURIComponent(username)}` : ''
      const headers = { ...getAuthHeader() }

      fetch(`${getApiBase()}/api/doctor/appointments${q}`, { headers })
        .then(r => r.ok ? r.json() : Promise.reject(r))
        .then(data => { this.appointments = (data || []).filter(a => a.status === 'Booked') })
        .catch(() => { this.appointments = [] })

      fetch(`${getApiBase()}/api/doctor/patients${q}`, { headers })
        .then(r => r.ok ? r.json() : Promise.reject(r))
        .then(data => { this.patients = data || [] })
        .catch(() => { this.patients = [] })
    },
    updateHistory(appointmentId) {
      if (this.$router) {
        this.$router.push({ name: 'editPatient', params: { appointmentId } })
      }
    },
    async markComplete(appointmentId) {
      if (!confirm('Mark appointment complete?')) return
      try {
        const headers = { ...getAuthHeader(), 'Content-Type': 'application/json' }
        const res = await fetch(`${getApiBase()}/api/doctor/appointment/${appointmentId}/complete`, {
          method: 'POST',
          headers
        })
        if (!res.ok) {
          const j = await res.json().catch(() => ({}))
          throw new Error(j.msg || 'Failed to mark complete')
        }
        alert('Appointment marked complete')
        this.appointments = this.appointments.filter(a => a.id !== appointmentId)
      } catch (e) {
        console.error('Error marking complete', e)
        const errorMsg = e.message || 'Failed to mark appointment complete'
        if (errorMsg.includes('update patient history')) {
          alert('Please update patient history first')
          this.updateHistory(appointmentId)
        } else {
          alert(errorMsg)
        }
      }
    },
    async cancelAppointment(appointmentId) {
      if (!confirm('Cancel appointment?')) return
      try {
        const headers = { ...getAuthHeader(), 'Content-Type': 'application/json' }
        const res = await fetch(`${getApiBase()}/api/doctor/appointment/${appointmentId}/cancel`, {
          method: 'POST',
          headers
        })
        if (!res.ok) {
          const j = await res.json().catch(() => ({}))
          throw new Error(j.msg || 'Failed to cancel')
        }
        alert('Appointment cancelled')
        this.appointments = this.appointments.filter(a => a.id !== appointmentId)
      } catch (e) {
        console.error('Error cancelling', e)
        alert(e.message || 'Failed to cancel appointment')
      }
    },

    viewPatient(patientId) {
      if (this.$router) {
        this.$router.push({ path: '/doctor_patient_history', query: { patient_id: patientId } })
      }
    },
    provideAvailability() {
      if (this.$router) {
        this.$router.push('/doctor_availability')
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.$router && this.$router.push('/login')
    }
  },
  mounted() {
    const storedName = localStorage.getItem('username')
    if (storedName) this.doctorName = storedName
    this.fetchData()
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.doctor-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.doctor-container {
  flex: 1;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* ========== WELCOME SECTION ========== */
.welcome-section {
  margin-bottom: 3rem;
  animation: slideDown 0.5s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.welcome-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.welcome-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* ========== DASHBOARD GRID ========== */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
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

.appointments-card {
  border-top-color: #667eea;
  grid-column: 1 / -1;
}

.patients-card {
  border-top-color: #764ba2;
}

.availability-card {
  border-top-color: #f093fb;
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
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

/* ========== APPOINTMENTS LIST ========== */
.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.appointment-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  /* border-left: 3px solid #667eea; */
  transition: all 0.3s ease;
}

.appointment-item:hover {
  background: #f0f2f9;
  transform: translateX(5px);
}

.appointment-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-weight: 700;
  flex-shrink: 0;
}

.appointment-info {
  flex: 1;
}

.appointment-info h4 {
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.appointment-time {
  font-size: 0.85rem;
  color: #7f8c8d;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #e8f4f8;
  color: #0c7fb1;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.8rem;
}

.appointment-actions {
  display: flex;
  gap: 0.5rem;
}

/* ========== PATIENTS LIST ========== */
.patients-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.patient-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  /* border-left: 3px solid #764ba2; */
  transition: all 0.3s ease;
}

.patient-item:hover {
  background: #f0f2f9;
  transform: translateX(5px);
}

.patient-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #e8eef7;
  border-radius: 50%;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.patient-info {
  flex: 1;
}

.patient-info h4 {
  color: #2c3e50;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.patient-id {
  font-size: 0.85rem;
  color: #7f8c8d;
}

/* ========== AVAILABILITY SECTION ========== */
.availability-content {
  text-align: center;
  padding: 1rem;
}

.availability-desc {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

/* ========== BUTTONS ========== */
.btn-primary {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  width: 100%;
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
  font-size: 0.85rem;
  background: transparent;
  border: 1px solid #ddd;
  font-weight: 600;
  white-space: nowrap;
}

.btn-action:hover {
  transform: translateY(-2px);
}

.btn-update {
  color: #3498db;
}

.btn-update:hover {
  background: #e0f2f9;
  border-color: #3498db;
}

.btn-complete {
  color: #1dd1a1;
}

.btn-complete:hover {
  background: #e8f9f5;
  border-color: #1dd1a1;
}

.btn-cancel {
  color: #e74c3c;
}

.btn-cancel:hover {
  background: #ffe0e0;
  border-color: #e74c3c;
}

.btn-view {
  color: #764ba2;
}

.btn-view:hover {
  background: #f4ecf7;
  border-color: #764ba2;
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
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  }

  .appointments-card {
    grid-column: 1 / -1;
  }
}

@media (max-width: 768px) {
  .doctor-container {
    padding: 1rem;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .welcome-content {
    padding: 1.5rem;
  }

  .welcome-title {
    font-size: 1.5rem;
  }

  .appointment-item,
  .patient-item {
    flex-wrap: wrap;
  }

  .appointment-actions {
    width: 100%;
    justify-content: space-between;
    order: 3;
  }

  .btn-action {
    padding: 0.4rem 0.6rem;
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .doctor-container {
    padding: 0.75rem;
  }

  .welcome-title {
    font-size: 1.2rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .appointment-number {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }

  .patient-avatar {
    width: 35px;
    height: 35px;
  }

  .btn-action {
    padding: 0.35rem 0.5rem;
    font-size: 0.7rem;
  }
}
</style>
