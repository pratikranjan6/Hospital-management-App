<template>
  <div class="user-wrapper">
    <UserNavBar />

    <div class="user-container">
      <!-- Welcome Header -->
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title"> Welcome, {{ userName }}</h1>
          <p class="welcome-subtitle">Book and manage your medical appointments</p>
        </div>
      </div>

      <!-- Dashboard Grid -->
      <div class="dashboard-grid">
        <!-- Departments Card -->
        <div class="dashboard-card departments-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title"> Available Departments</h3>
              <p class="card-subtitle">{{ departments.length }} departments</p>
            </div>
          </div>
          <div class="card-body">
            <div v-if="loading" class="loading-state">
              <div class="spinner"></div>
              <p>Loading departments...</p>
            </div>
            <div v-else-if="departments.length === 0" class="empty-state">
              <p>No departments available</p>
            </div>
            <div v-else class="departments-grid">
              <div v-for="department in departments" :key="department.id" class="dept-card">
                <div class="dept-header">
                  <h4>{{ department.name }}</h4>
                </div>
                <div class="dept-body">
                  <p class="dept-description">{{ department.description }}</p>
                  <button @click="viewDepartmentDetails(department)" class="btn-action btn-view">View Details</button>
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
              <p class="card-subtitle">{{ filteredAppointments.length }} appointments</p>
            </div>
          </div>
          <div class="card-body">
            <div v-if="loadingAppointments" class="loading-state">
              <div class="spinner"></div>
              <p>Loading appointments...</p>
            </div>
            <div v-else-if="filteredAppointments.length === 0" class="empty-state">
              <p>No upcoming appointments</p>
            </div>
            <div v-else class="appointments-table">
              <div class="table-header">
                <div class="col-no">Sr No.</div>
                <div class="col-doctor">Doctor</div>
                <div class="col-dept">Department</div>
                <div class="col-date">Date</div>
                <div class="col-time">Time</div>
                <div class="col-action">Action</div>
              </div>
              <div v-for="(appointment, index) in filteredAppointments" :key="appointment.id" class="table-row">
                <div class="col-no">{{ index + 1 }}</div>
                <div class="col-doctor">Dr. {{ appointment.doctor_name }}</div>
                <div class="col-dept">{{ appointment.department_name }}</div>
                <div class="col-date">{{ formatDate(appointment.appointment_date) }}</div>
                <div class="col-time">{{ formatTime(appointment.appointment_date) }}</div>
                <div class="col-action">
                  <button
                    v-if="appointment.status !== 'Cancelled'"
                    @click="cancelAppointment(appointment.id)"
                    class="btn-action btn-cancel"
                    :disabled="cancellationLoading === appointment.id"
                  >
                    {{ cancellationLoading === appointment.id ? 'Cancelling...' : 'Cancel' }}
                  </button>
                  <span v-else class="status-badge">Cancelled</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import UserNavBar from './UserNavBar.vue'
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'UserDashboard',
  components: { UserNavBar },
  data() {
    return {
      userName: 'User',
      departments: [],
      appointments: [],
      loading: true,
      loadingAppointments: true,
      cancellationLoading: null
    }
  },
  computed: {
    filteredAppointments() {
      return this.appointments.filter(apt => apt.status === 'Booked')
    }
  },
  methods: {
    async fetchDepartments() {
      try {
        this.loading = true
        const response = await fetch(`${getApiBase()}/api/departments`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to fetch departments')
        }

        this.departments = await response.json()
      } catch (error) {
        console.error('Error fetching departments:', error)
        alert('Failed to fetch departments')
      } finally {
        this.loading = false
      }
    },

    async exportHistory() {
      try {
        const response = await fetch(`${getApiBase()}/api/patient/export_history`, {
          method: 'POST',
          headers: getAuthHeader()
        })
        if (!response.ok) {
          throw new Error('Export request failed')
        }
        alert('Export started. You will receive an email when it completes.')

        const checkStatus = async () => {
          try {
            const s = await fetch(`${getApiBase()}/api/patient/export_status`, {
              method: 'GET',
              headers: getAuthHeader()
            })
            if (s.ok) {
              const data = await s.json()
              if (data.done) {
                alert('Export completed; check your email.')
              } else {
                setTimeout(checkStatus, 5000)
              }
            } else {
              setTimeout(checkStatus, 5000)
            }
          } catch (e) {
            setTimeout(checkStatus, 5000)
          }
        }
        checkStatus()
      } catch (err) {
        console.error('Error starting export:', err)
        alert('Failed to start export')
      }
    },

    async fetchUserAppointments() {
      try {
        this.loadingAppointments = true
        const response = await fetch(`${getApiBase()}/api/user/appointments`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to fetch appointments')
        }

        this.appointments = await response.json()
      } catch (error) {
        console.error('Error fetching appointments:', error)
        alert('Failed to fetch appointments')
      } finally {
        this.loadingAppointments = false
      }
    },

    async fetchUserInfo() {
      try {
        const response = await fetch(`${getApiBase()}/api/login`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (response.ok) {
          const data = await response.json()
          this.userName = data.user?.full_name || 'User'
        }
      } catch (error) {
        console.error('Error fetching user info:', error)
      }
    },

    async cancelAppointment(appointmentId) {
      if (!confirm('Are you sure you want to cancel this appointment?')) {
        return
      }

      try {
        this.cancellationLoading = appointmentId
        const response = await fetch(
          `${getApiBase()}/api/user/appointment/${appointmentId}`,
          {
            method: 'DELETE',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          throw new Error('Failed to cancel appointment')
        }

        const appointment = this.appointments.find(apt => apt.id === appointmentId)
        if (appointment) {
          appointment.status = 'Cancelled'
        }

        alert('Appointment cancelled successfully')
      } catch (error) {
        console.error('Error cancelling appointment:', error)
        alert('Failed to cancel appointment')
      } finally {
        this.cancellationLoading = null
      }
    },

    viewDepartmentDetails(department) {
      this.$router.push({
        path: `/department/${department.id}`,
        query: { department: encodeURIComponent(JSON.stringify(department)) }
      })
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-GB')
    },

    formatTime(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      return `${hours}:${minutes}`
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      this.$router.push('/login')
    }
  },
  mounted() {
    this.fetchDepartments()
    this.fetchUserAppointments()
    this.fetchUserInfo()
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.user-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.user-container {
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

.departments-card {
  border-top-color: #667eea;
}

.appointments-card {
  border-top-color: #764ba2;
  grid-column: 1 / -1;
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

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #7f8c8d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f0f0f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ========== DEPARTMENTS GRID ========== */
.departments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.dept-card {
  background: linear-gradient(135deg, #f9f9f9 0%, #f0f2f9 100%);
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e8eef7;
}

.dept-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.dept-header {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.dept-header h4 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
}

.dept-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dept-description {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin: 0;
  flex: 1;
}

/* ========== APPOINTMENTS TABLE ========== */
.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: grid;
  grid-template-columns: 80px 1.5fr 1.2fr 120px 100px 120px;
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
  grid-template-columns: 80px 1.5fr 1.2fr 120px 100px 120px;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  /* border-left: 3px solid #764ba2; */
  transition: all 0.2s ease;
  align-items: center;
}

.table-row:hover {
  background: #f0f2f9;
  transform: translateX(5px);
}

.col-no,
.col-doctor,
.col-dept,
.col-date,
.col-time,
.col-action {
  font-size: 0.95rem;
  color: #2c3e50;
}

/* ========== BUTTONS ========== */
.btn-action {
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.85rem;
  background: transparent;
  border: 1px solid #ddd;
  white-space: nowrap;
}

.btn-action:hover {
  transform: translateY(-2px);
}

.btn-view {
  color: #667eea;
  border-color: #667eea;
  width: 100%;
}

.btn-view:hover {
  background: #e8eef7;
  border-color: #667eea;
}

.btn-cancel {
  color: #e74c3c;
  border-color: #e74c3c;
}

.btn-cancel:hover:not(:disabled) {
  background: #ffe0e0;
  border-color: #e74c3c;
}

.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ========== STATUS BADGE ========== */
.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #e8eef7;
  color: #667eea;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
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

@media (max-width: 968px) {
  .table-header,
  .table-row {
    grid-template-columns: 60px 1.2fr 1fr 100px 80px 100px;
  }
}

@media (max-width: 768px) {
  .user-container {
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

  .departments-grid {
    grid-template-columns: 1fr;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .col-no,
  .col-doctor,
  .col-dept,
  .col-date,
  .col-time,
  .col-action {
    display: flex;
    justify-content: space-between;
  }

  .btn-action {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .user-container {
    padding: 0.75rem;
  }

  .welcome-title {
    font-size: 1.2rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .table-header,
  .table-row {
    padding: 0.75rem;
  }

  .btn-action {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
  }
}
</style>
