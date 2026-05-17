<template>
  <div class="user-wrapper">
    <UserNavBar />

    <div class="user-container">
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title">Welcome, {{ userName }}</h1>
          <p class="welcome-subtitle">Book and manage your medical appointments</p>
        </div>
      </div>

      <div class="dashboard-grid">
        <div class="dashboard-card departments-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title">Available Departments</h3>
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

        <div class="dashboard-card appointments-card">
          <div class="card-header">
            <div class="header-content">
              <h3 class="card-title">Upcoming Appointments</h3>
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
    <FloatingAIButton />
  </div>
</template>

<script>
import UserNavBar from './UserNavBar.vue'
import FloatingAIButton from './FloatingAIButton.vue'
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'UserDashboard',
  components: { UserNavBar, FloatingAIButton },
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
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.user-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f2e8d8;
  display: flex;
  flex-direction: column;
}

.user-container {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.welcome-section {
  margin-bottom: 2rem;
}

.welcome-content {
  background: #fffdf7;
  color: #3d362f;
  padding: 2rem;
  border-radius: 24px;
  border: 1px solid #d8c8b0;
  box-shadow: 0 18px 30px rgba(0, 0, 0, 0.05);
}

.welcome-title {
  font-size: 3rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 1rem;
  color: #6d5f53;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
  gap: 1.75rem;
}

.dashboard-card {
  background: #fffdf7;
  border-radius: 24px;
  border: 1px solid #d8c8b0;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

/* .dashboard-card:hover {
  transform: translateY(-3px);
} */

/* .departments-card {
  border-top: 4px solid #8f7b65;
} */

/* .appointments-card {
  border-top: 4px solid #a68a72;
} */

.card-header {
  padding: 1.5rem;
  background: #f4e9db;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dacbb8;
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 800;
  color: #3d362f;
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.95rem;
  color: #7d6d5f;
}

.card-body {
  padding: 1.5rem;
}

.loading-state {
  text-align: center;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #7d6d5f;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e3d3c1;
  border-top-color: #8f7b65;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.departments-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
}

.dept-card {
  background: #fff9f1;
  border-radius: 18px;
  overflow: hidden;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  border: 1px solid #e2d1be;
}

.dept-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.06);
}

.dept-header {
  padding: 1rem;
  background: #f3eadf;
  color: #3d362f;
}

.dept-header h4 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
}

.dept-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}

.dept-description {
  color: #6d5f53;
  font-size: 0.95rem;
  margin: 0;
  flex: 1;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: grid;
  grid-template-columns: 80px 1.5fr 1.2fr 120px 100px 120px;
  gap: 1rem;
  padding: 1rem;
  background: #f4e9db;
  color: #3d362f;
  font-weight: 700;
  border-radius: 16px;
  margin-bottom: 0.7rem;
}

.table-row {
  display: grid;
  grid-template-columns: 80px 1.5fr 1.2fr 120px 100px 120px;
  gap: 1rem;
  padding: 1rem;
  background: #fff9f1;
  border-radius: 16px;
  margin-bottom: 0.55rem;
  border: 1px solid #e6d6c5;
  transition: background 0.25s ease, transform 0.25s ease;
  align-items: center;
}

.table-row:hover {
  background: #f7eee5;
  transform: translateX(3px);
}

.col-no,
.col-doctor,
.col-dept,
.col-date,
.col-time,
.col-action {
  font-size: 0.95rem;
  color: #3d362f;
}

.btn-action {
  padding: 0.7rem 1rem;
  border: 1px solid #d1c2b3;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.25s ease, transform 0.25s ease;
  font-weight: 700;
  font-size: 0.85rem;
  background: transparent;
  color: #3d362f;
  white-space: nowrap;
}

.btn-action:hover {
  background: #f3eadf;
  transform: translateY(-2px);
}

.btn-view {
  color: #3d362f;
  border-color: #3d362f;
  background: #f9f1e8;
  width: 100%;
}

.btn-cancel {
  color: #8a2f2a;
  border-color: #8a2f2a;
  background: rgba(138, 47, 42, 0.1);
}

.btn-cancel:hover:not(:disabled) {
  background: rgba(138, 47, 42, 0.18);
}

.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.status-badge {
  display: inline-block;
  padding: 0.55rem 1rem;
  background: #56493f;
  color: #ffffff;
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.85rem;
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #6d5f53;
  font-style: italic;
  background: #fff7f0;
  border-radius: 16px;
  border: 1px dashed #d7c7b5;
}

@media (max-width: 1200px) {
  .dashboard-grid {
    grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
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

  .dept-card {
    width: 100%;
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
    font-size: 1.8rem;
  }

  .card-title {
    font-size: 1.05rem;
  }

  .table-header,
  .table-row {
    padding: 0.75rem;
  }

  .btn-action {
    padding: 0.55rem 0.85rem;
    font-size: 0.75rem;
  }
}
</style>
