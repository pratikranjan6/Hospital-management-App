<template>
  <div class="department-info">
    <div class="department-header">
      <h1>{{ department.name }}</h1>
      <div class="header-actions">
        <router-link to="/history" class="action-link">History</router-link>
        <span class="divider">|</span>
        <button @click="logout" class="logout-btn">logout</button>
      </div>
    </div>

    <button @click="goBack" class="back-btn">← Back to Dashboard</button>

    <div class="overview-section">
      <h2>Overview</h2>
      <p>{{ department.description }}</p>
    </div>

    <div class="doctors-section">
      <h2>Doctors' list</h2>
      <div v-if="loading" class="loading">Loading doctors...</div>
      <div v-else-if="doctors.length === 0" class="no-data">No doctors available in this department</div>
      <div v-else class="doctors-table-container">
        <table class="doctors-table">
          <tbody>
            <tr v-for="doctor in doctors" :key="doctor.id">
              <td class="doctor-name">{{ doctor.name }}</td>
              <td class="doctor-actions">
                <button @click="checkAvailability(doctor)" class="availability-btn">
                  check availability
                </button>
                <button @click="viewDoctorDetails(doctor)" class="details-btn">
                  view details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showDoctorModal" class="modal-overlay" @click.self="closeDoctorModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedDoctor.name }}</h3>
          <button @click="closeDoctorModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <p><strong>Specialization:</strong> {{ selectedDoctor.specialization }}</p>
          <p><strong>Qualification:</strong> {{ selectedDoctor.qualification }}</p>
          <p><strong>Experience:</strong> {{ selectedDoctor.experience }} years</p>
        </div>
        <div class="modal-footer">
          <button @click="closeDoctorModal" class="btn-primary">Close</button>
        </div>
      </div>
    </div>

    <div v-if="showAvailabilityModal" class="modal-overlay" @click.self="closeAvailabilityModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedDoctor.name }} - Availability</h3>
          <button @click="closeAvailabilityModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <p v-if="doctorAvailability.length === 0" class="no-data">No availability information available</p>
          <div v-else class="availability-list">
            <div v-for="availability in doctorAvailability" :key="availability.id" class="availability-item">
              <p><strong>Date:</strong> {{ formatDate(availability.date) }}</p>
              <p><strong>Status:</strong> <span class="status-badge" :class="availability.status.toLowerCase()">{{ availability.status }}</span></p>
              <p v-if="availability.start_time"><strong>Time:</strong> {{ availability.start_time }} - {{ availability.end_time }}</p>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeAvailabilityModal" class="btn-primary">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'DepartmentInfo',
  data() {
    return {
      department: {},
      doctors: [],
      loading: true,
      showDoctorModal: false,
      showAvailabilityModal: false,
      selectedDoctor: {},
      doctorAvailability: []
    }
  },
  methods: {
    async fetchDepartmentData() {
      try {
        const departmentId = this.$route.params.id
        if (!departmentId) {
          const sessionDept = this.$route.query.department
          if (sessionDept) {
            this.department = JSON.parse(decodeURIComponent(sessionDept))
          } else {
            this.$router.push('/user_dashboard')
            return
          }
        }
      } catch (error) {
        console.error('Error parsing department:', error)
        this.$router.push('/user_dashboard')
      }
    },

    async fetchDoctors() {
      try {
        this.loading = true
        const departmentId = this.department.id

        const response = await fetch(
          `${getApiBase()}/api/department/${departmentId}/doctors`,
          {
            method: 'GET',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          throw new Error('Failed to fetch doctors')
        }

        this.doctors = await response.json()
      } catch (error) {
        console.error('Error fetching doctors:', error)
        this.$toast?.error?.('Failed to fetch doctors')
      } finally {
        this.loading = false
      }
    },

    async fetchDoctorAvailability(doctorId) {
      try {
        const response = await fetch(
          `${getApiBase()}/api/doctor/${doctorId}/availability`,
          {
            method: 'GET',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          this.doctorAvailability = []
          return
        }

        this.doctorAvailability = await response.json()
      } catch (error) {
        console.error('Error fetching availability:', error)
        this.doctorAvailability = []
      }
    },

    viewDoctorDetails(doctor) {
      this.selectedDoctor = doctor
      this.showDoctorModal = true
    },

    closeDoctorModal() {
      this.showDoctorModal = false
      this.selectedDoctor = {}
    },

    async checkAvailability(doctor) {
      this.$router.push({
        name: 'bookAppointment',
        params: { doctorId: doctor.id },
        query: { doctorName: doctor.name }
      })
    },

    closeAvailabilityModal() {
      this.showAvailabilityModal = false
      this.selectedDoctor = {}
      this.doctorAvailability = []
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-GB')
    },

    goBack() {
      this.$router.back()
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      this.$router.push('/login')
    }
  },

  mounted() {
    const passedDept = this.$route.params.department
    if (passedDept) {
      try {
        this.department = typeof passedDept === 'string' ? JSON.parse(passedDept) : passedDept
      } catch (error) {
        this.department = passedDept
      }
    }

    if (this.$route.query.department) {
      try {
        this.department = JSON.parse(decodeURIComponent(this.$route.query.department))
      } catch (error) {
      }
    }

    if (this.department && this.department.id) {
      this.fetchDoctors()
    } else {
      this.$router.push('/user_dashboard')
    }
  }
}
</script>

<style scoped>
.department-info {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
  width: 100%;
}

.department-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.department-header h1 {
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

.back-btn {
  padding: 8px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 20px;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #5a6268;
}

.overview-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.overview-section h2 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 22px;
  color: #333;
  font-weight: 600;
}

.overview-section p {
  margin: 0;
  color: #666;
  line-height: 1.6;
  font-size: 15px;
  text-align: justify;
}

.doctors-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.doctors-section h2 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 22px;
  color: #333;
  font-weight: 600;
}

.doctors-table-container {
  overflow-x: auto;
}

.doctors-table {
  width: 100%;
  border-collapse: collapse;
  border: 2px solid #333;
}

.doctors-table tbody tr {
  border-bottom: 1px solid #ddd;
}

.doctors-table tbody tr:last-child {
  border-bottom: 2px solid #333;
}

.doctors-table td {
  padding: 15px;
}

.doctor-name {
  text-align: left;
  color: #999;
  font-size: 15px;
  flex: 1;
  min-width: 150px;
}

.doctor-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.availability-btn,
.details-btn {
  padding: 8px 16px;
  border: 2px solid #007bff;
  background-color: white;
  color: #007bff;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s;
  white-space: nowrap;
}

.availability-btn:hover,
.details-btn:hover {
  background-color: #007bff;
  color: white;
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
  margin: 0 0 15px 0;
}

.modal-body p:last-child {
  margin-bottom: 0;
}

.availability-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.availability-item {
  border: 1px solid #dee2e6;
  padding: 12px;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.availability-item p {
  margin: 0 0 8px 0;
  font-size: 14px;
}

.availability-item p:last-child {
  margin-bottom: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.available {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.unavailable,
.status-badge.not\ available {
  background-color: #f8d7da;
  color: #721c24;
}

.status-badge.morning,
.status-badge.afternoon,
.status-badge.evening {
  background-color: #d1ecf1;
  color: #0c5460;
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
  .department-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .header-actions {
    justify-content: center;
  }

  .doctor-actions {
    flex-direction: column;
    align-items: flex-end;
  }

  .availability-btn,
  .details-btn {
    width: 100%;
    text-align: center;
  }
}
</style>
