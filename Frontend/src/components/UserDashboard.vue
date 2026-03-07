<template>
  <div class="user-dashboard">
    <div class="dashboard-header">
      <h1>Patients' Dashboard</h1>
      <div class="header-actions">
        <router-link to="/edit-profile" class="action-link">edit profile</router-link>
        <span class="divider">|</span>
        <router-link to="/history" class="action-link">History</router-link>
        <span class="divider">|</span>
        <button @click="exportHistory" class="action-link">Export CSV</button>
        <span class="divider">|</span>
        <button @click="logout" class="logout-btn">logout</button>
      </div>
    </div>

    <div class="welcome-section">
      <h2>Welcome {{ userName }}</h2>
    </div>

    <div class="departments-section">
      <h3>Departments</h3>
      <div v-if="loading" class="loading">Loading departments...</div>
      <div v-else-if="departments.length === 0" class="no-data">No departments available</div>
      <div v-else class="departments-list">
        <div v-for="department in departments" :key="department.id" class="department-card">
          <h4>{{ department.name }}</h4>
          <p>{{ department.description }}</p>
          <button @click="viewDepartmentDetails(department)" class="view-details-btn">
            view details
          </button>
        </div>
      </div>
    </div>

    <div class="appointments-section">
      <h3>Upcoming Appointments</h3>
      <div v-if="loadingAppointments" class="loading">Loading appointments...</div>
      <div v-else-if="filteredAppointments.length === 0" class="no-data">
        No upcoming appointments
      </div>
      <div v-else class="appointments-table-container">
        <table class="appointments-table">
          <thead>
            <tr>
              <th>Sr No.</th>
              <th>Doctor Name</th>
              <th>Department</th>
              <th>Date</th>
              <th>Time</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(appointment, index) in filteredAppointments" :key="appointment.id">
              <td>{{ index + 1 }}.</td>
              <td>{{ appointment.doctor_name }}</td>
              <td>{{ appointment.department_name }}</td>
              <td>{{ formatDate(appointment.appointment_date) }}</td>
              <td>{{ formatTime(appointment.appointment_date) }}</td>
              <td>
                <button
                  v-if="appointment.status !== 'Cancelled'"
                  @click="cancelAppointment(appointment.id)"
                  class="cancel-btn"
                  :disabled="cancellationLoading === appointment.id"
                >
                  {{ cancellationLoading === appointment.id ? 'Cancelling...' : 'cancel' }}
                </button>
                <span v-else class="cancelled-tag">Cancelled</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'UserDashboard',
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
        this.$toast?.error?.('Failed to fetch departments')
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
        this.$toast?.success?.('Export started. You will receive an email when it completes.')

        // poll status every 5 seconds until done
        const checkStatus = async () => {
          try {
            const s = await fetch(`${getApiBase()}/api/patient/export_status`, {
              method: 'GET',
              headers: getAuthHeader()
            })
            if (s.ok) {
              const data = await s.json()
              if (data.done) {
                this.$toast?.success?.('Export completed; check your email.')
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
        this.$toast?.error?.('Failed to start export')
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
        this.$toast?.error?.('Failed to fetch appointments')
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

        this.$toast?.success?.('Appointment cancelled successfully')
      } catch (error) {
        console.error('Error cancelling appointment:', error)
        this.$toast?.error?.('Failed to cancel appointment')
      } finally {
        this.cancellationLoading = null
      }
    },

    viewDepartmentDetails(department) {
      console.log('navigating to department', department.id)
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
.user-dashboard {
  max-width: 2000px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  margin: 0;
  font-size: 28px;
  color: #333;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.action-link {
  color: #007bff;
  text-decoration: none;
  cursor: pointer;
  font-size: 14px;
  transition: color 0.3s;
}

.action-link:hover {
  color: #0056b3;
}

.divider {
  color: #999;
}

.logout-btn {
  background: none;
  border: none;
  color: #007bff;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
  transition: color 0.3s;
}

.logout-btn:hover {
  color: #0056b3;
}

.welcome-section {
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-section h2 {
  margin: 0;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.departments-section {
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.departments-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.departments-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.department-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  background-color: #fafafa;
  transition: all 0.3s;
}

.department-card:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
}

.department-card h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.department-card p {
  margin: 0 0 15px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.4;
}

.view-details-btn {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.view-details-btn:hover {
  background-color: #0056b3;
}

.appointments-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.appointments-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.appointments-table-container {
  overflow-x: auto;
}

.appointments-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.appointments-table thead {
  background-color: #f8f9fa;
}

.appointments-table th {
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #dee2e6;
  color: #333;
  font-weight: 600;
}

.appointments-table td {
  padding: 12px;
  border-bottom: 1px solid #dee2e6;
  color: #666;
}

.appointments-table tbody tr:hover {
  background-color: #f9f9f9;
}

.cancel-btn {
  padding: 6px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.cancel-btn:hover:not(:disabled) {
  background-color: #c82333;
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancelled-tag {
  color: #6c757d;
  font-style: italic;
}

.loading,
.no-data {
  text-align: center;
  padding: 30px;
  color: #666;
  font-size: 16px;
}

.loading {
  color: #007bff;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #dee2e6;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 22px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 28px;
  color: #999;
  cursor: pointer;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  color: #666;
  line-height: 1.6;
}

.modal-body p {
  margin: 0 0 10px 0;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #dee2e6;
  text-align: right;
}

.btn-primary {
  padding: 8px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .header-actions {
    justify-content: center;
  }

  .departments-list {
    grid-template-columns: 1fr;
  }

  .appointments-table {
    font-size: 12px;
  }

  .appointments-table th,
  .appointments-table td {
    padding: 8px 4px;
  }
}
</style>
