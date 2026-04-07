<template>
  <div class="department-wrapper">
    <!-- Header with Back Button -->
    <div class="department-header">
      <button @click="goBack" class="btn-back">
        <span class="back-arrow">←</span> Back to Dashboard
      </button>
      <h1 class="department-title">{{ department.name }}</h1>
      <button @click="logout" class="btn-logout">Logout</button>
    </div>

    <div class="department-container">
      <!-- Overview Section -->
      <div class="overview-card">
        <div class="card-header">
          <h2 class="card-title"> Department Overview</h2>
        </div>
        <div class="card-body">
          <p class="overview-text">{{ department.description }}</p>
        </div>
      </div>

      <!-- Doctors List Section -->
      <div class="doctors-card">
        <div class="card-header">
          <h2 class="card-title"> Doctors in this Department</h2>
          <p class="card-subtitle">{{ doctors.length }} doctors available</p>
        </div>

        <!-- Search Bar -->
        <div class="search-section">
          <form class="search-form" @submit.prevent="searchDoctors">
            <input
              v-model="searchQuery"
              class="search-input"
              type="search"
              placeholder="Search doctors by name..."
              aria-label="Search doctors"
            />
            <button class="btn-search" type="submit"> Search</button>
          </form>
        </div>

        <div class="card-body">
          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading doctors...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="doctors.length === 0" class="empty-state">
            <p>No doctors available in this department</p>
          </div>

          <!-- Doctors List -->
          <div v-else class="doctors-list">
            <div v-for="doctor in doctors" :key="doctor.id" class="doctor-item">
              <div class="doctor-info">
                <h4 class="doctor-name">Dr. {{ doctor.name }}</h4>
                <p class="doctor-specialty">{{ doctor.specialization }}</p>
              </div>
              <div class="doctor-actions">
                <button @click="viewDoctorDetails(doctor)" class="btn-action btn-details">View Profile</button>
                <button @click="checkAvailability(doctor)" class="btn-action btn-book">Book Appointment</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Doctor Details Modal -->
    <div v-if="showDoctorModal" class="modal-overlay" @click.self="closeDoctorModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Dr. {{ selectedDoctor.name }}</h3>
          <button class="modal-close" @click="closeDoctorModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-group">
            <span class="detail-label">Specialization:</span>
            <span class="detail-value">{{ selectedDoctor.specialization }}</span>
          </div>
          <div class="detail-group">
            <span class="detail-label">Qualification:</span>
            <span class="detail-value">{{ selectedDoctor.qualification }}</span>
          </div>
          <div class="detail-group">
            <span class="detail-label">Experience:</span>
            <span class="detail-value">{{ selectedDoctor.experience }} years</span>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-modal-close" @click="closeDoctorModal">Close</button>
        </div>
      </div>
    </div>
    <div v-if="showDoctorModal" class="modal-backdrop"></div>

    <!-- Availability Modal -->
    <div v-if="showAvailabilityModal" class="modal-overlay" @click.self="closeAvailabilityModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Dr. {{ selectedDoctor.name }} - Availability</h3>
          <button class="modal-close" @click="closeAvailabilityModal">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="doctorAvailability.length === 0" class="empty-modal-state">
            <p>No availability information available</p>
          </div>
          <div v-else class="availability-list">
            <div v-for="availability in doctorAvailability" :key="availability.id" class="availability-item">
              <div class="availability-date">
                📅 {{ formatDate(availability.date) }}
              </div>
              <div class="availability-details">
                <span class="status-badge" :class="getStatusBadgeClass(availability.status)">
                  {{ availability.status }}
                </span>
                <span v-if="availability.start_time" class="time-slot">
                  ⏰ {{ availability.start_time }} - {{ availability.end_time }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-modal-close" @click="closeAvailabilityModal">Close</button>
        </div>
      </div>
    </div>
    <div v-if="showAvailabilityModal" class="modal-backdrop"></div>
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
      searchQuery: '',
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

    async searchDoctors() {
      try {
        this.loading = true
        const departmentId = this.department.id
        let url = `${getApiBase()}/api/department/${departmentId}/doctors`
        if (this.searchQuery.trim()) {
          url += `?q=${encodeURIComponent(this.searchQuery.trim())}`
        }

        const response = await fetch(url, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to search doctors')
        }

        this.doctors = await response.json()
      } catch (error) {
        console.error('Error searching doctors:', error)
        this.$toast?.error?.('Failed to search doctors')
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

    getStatusBadgeClass(status) {
      const lowerStatus = status.toLowerCase()
      if (lowerStatus === 'available') return 'bg-success'
      if (lowerStatus === 'unavailable' || lowerStatus === 'not available') return 'bg-danger'
      return 'bg-info'
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.department-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

/* ========== HEADER ========== */
.department-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  position: sticky;
  top: 0;
  z-index: 10;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.4);
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-back:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.6);
  transform: translateX(-3px);
}

.back-arrow {
  font-size: 1.2rem;
}

.department-title {
  font-size: 1.8rem;
  font-weight: 700;
  flex: 1;
  text-align: center;
  margin: 0;
}

.btn-logout {
  padding: 0.6rem 1.5rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.6);
  transform: translateY(-2px);
}

/* ========== CONTAINER ========== */
.department-container {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
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
.overview-card,
.doctors-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
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

/* .overview-card:hover,
.doctors-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  transform: translateY(-5px);
} */

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  border-bottom: 2px solid #e0e6ed;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
}

/* ========== OVERVIEW TEXT ========== */
.overview-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #2c3e50;
  text-align: justify;
  margin: 0;
}

/* ========== SEARCH SECTION ========== */
.search-section {
  padding: 1.5rem;
  background: #f9f9f9;
  border-bottom: 1px solid #e0e6ed;
}

.search-form {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e0e6ed;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-input::placeholder {
  color: #bdc3c7;
}

.btn-search {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* ========== DOCTORS LIST ========== */
.doctors-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.doctor-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
  background: linear-gradient(135deg, #f9f9f9 0%, #f5f7fa 100%);
  border-radius: 10px;
  transition: all 0.3s ease;
}

/* .doctor-item:hover {
  background: linear-gradient(135deg, #f0f2f9 0%, #e8eef7 100%);
  transform: translateX(5px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
} */

.doctor-info {
  flex: 1;
}

.doctor-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 0.25rem 0;
}

.doctor-specialty {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
  font-style: italic;
}

.doctor-actions {
  display: flex;
  gap: 0.75rem;
  margin-left: 1rem;
}

/* ========== BUTTONS ========== */
.btn-action {
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-details {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-details:hover {
  background: #e8eef7;
  transform: translateY(-2px);
}

.btn-book {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.btn-book:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 3rem 2rem;
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

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #7f8c8d;
  font-style: italic;
  background: #f9f9f9;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

/* ========== MODAL ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 500px;
  animation: slideUp 0.3s ease-out;
  z-index: 1001;
  position: relative;
  overflow: hidden;
}

.modal-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
}

.modal-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  transform: scale(1.2) rotate(90deg);
}

.modal-body {
  padding: 2rem;
}

.detail-group {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem 0;
  border-bottom: 1px solid #e0e6ed;
}

.detail-group:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 700;
  color: #2c3e50;
  min-width: 120px;
}

.detail-value {
  color: #7f8c8d;
  text-align: right;
  flex: 1;
}

.empty-modal-state {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
  font-style: italic;
  background: #f9f9f9;
  border-radius: 8px;
}

.availability-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.availability-item {
  padding: 1rem;
  background: linear-gradient(135deg, #f9f9f9 0%, #f5f7fa 100%);
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.availability-date {
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.availability-details {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.status-badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.8rem;
}

.status-badge.bg-success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.status-badge.bg-danger {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.status-badge.bg-info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

.time-slot {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.modal-footer {
  padding: 1rem 2rem;
  background: #f9f9f9;
  border-top: 1px solid #e0e6ed;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-modal-close {
  padding: 0.6rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-modal-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .department-header {
    flex-direction: column;
    padding: 1rem;
    gap: 1rem;
    text-align: center;
  }

  .department-title {
    font-size: 1.4rem;
  }

  .btn-back,
  .btn-logout {
    width: 100%;
  }

  .department-container {
    padding: 1rem;
  }

  .doctor-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .doctor-actions {
    width: 100%;
    flex-direction: column;
    margin-left: 0;
  }

  .btn-action {
    width: 100%;
    text-align: center;
  }

  .search-form {
    flex-direction: column;
  }

  .btn-search {
    width: 100%;
  }

  .modal-content {
    width: 95%;
    max-width: 450px;
  }

  .detail-group {
    flex-direction: column;
    gap: 0.5rem;
  }

  .detail-label {
    min-width: auto;
  }

  .detail-value {
    text-align: left;
  }

  .availability-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .department-header {
    padding: 0.75rem;
  }

  .department-title {
    font-size: 1.2rem;
  }

  .btn-back,
  .btn-logout {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .doctor-item {
    padding: 1rem;
  }

  .btn-action {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .modal-header h3 {
    font-size: 1.1rem;
  }
}
</style>