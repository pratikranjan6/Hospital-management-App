<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">Patients' Dashboard</span>
        <div class="navbar-nav ms-auto">
          <router-link to="/edit-profile" class="nav-link">Edit Profile</router-link>
          <span class="nav-link">|</span>
          <router-link to="/history" class="nav-link">History</router-link>
          <span class="nav-link">|</span>
          <button @click="logout" class="btn btn-outline-danger btn-sm">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="card mb-4">
        <div class="card-body">
          <h2 class="card-title">Welcome {{ userName }}</h2>
        </div>
      </div>

      <div class="card mb-4">
        <div class="card-header">
          <h3 class="mb-0">Departments</h3>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center text-primary">Loading departments...</div>
          <div v-else-if="departments.length === 0" class="alert alert-info">No departments available</div>
          <div v-else class="row">
            <div v-for="department in departments" :key="department.id" class="col-md-6 mb-3">
              <div class="card h-100">
                <div class="card-body d-flex flex-column">
                  <h5 class="card-title">{{ department.name }}</h5>
                  <p class="card-text flex-grow-1">{{ department.description }}</p>
                  <button @click="viewDepartmentDetails(department)" class="btn btn-primary mt-auto">View Details</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="mb-0">Upcoming Appointments</h3>
        </div>
        <div class="card-body">
          <div v-if="loadingAppointments" class="text-center text-primary">Loading appointments...</div>
          <div v-else-if="filteredAppointments.length === 0" class="alert alert-info">No upcoming appointments</div>
          <div v-else class="table-responsive">
            <table class="table table-striped">
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
                  <td>{{ index + 1 }}</td>
                  <td>{{ appointment.doctor_name }}</td>
                  <td>{{ appointment.department_name }}</td>
                  <td>{{ formatDate(appointment.appointment_date) }}</td>
                  <td>{{ formatTime(appointment.appointment_date) }}</td>
                  <td>
                    <button
                      v-if="appointment.status !== 'Cancelled'"
                      @click="cancelAppointment(appointment.id)"
                      class="btn btn-danger btn-sm"
                      :disabled="cancellationLoading === appointment.id"
                    >
                      {{ cancellationLoading === appointment.id ? 'Cancelling...' : 'Cancel' }}
                    </button>
                    <span v-else class="badge bg-secondary">Cancelled</span>
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
body {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.table thead th {
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}
</style>
