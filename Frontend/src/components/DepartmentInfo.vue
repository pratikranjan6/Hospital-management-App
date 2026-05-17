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
  background: #f2e8d8;
  display: flex;
  flex-direction: column;
}

/* ========== HEADER ========== */
.department-header {
  background: #fffdf7;
  color: #3d362f;
  padding: 1.5rem 2rem;
  border-bottom: 2px solid #d8c8b0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 10;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(143, 123, 101, 0.1);
  color: #8f7b65;
  border: 2px solid #d8c8b0;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-back:hover {
  background: rgba(143, 123, 101, 0.15);
  border-color: #8f7b65;
  transform: translateX(-3px);
}

.back-arrow {
  font-size: 1.2rem;
}

.department-title {
  font-size: 1.8rem;
  font-weight: 800;
  flex: 1;
  text-align: center;
  margin: 0;
  color: #3d362f;
}

.btn-logout {
  padding: 0.6rem 1.5rem;
  background: rgba(143, 123, 101, 0.1);
  color: #8f7b65;
  border: 2px solid #d8c8b0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-logout:hover {
  background: rgba(143, 123, 101, 0.15);
  border-color: #8f7b65;
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
  background: #fffdf7;
  border-radius: 24px;
  border: 1px solid #d8c8b0;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
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
  background: #f4e9db;
  border-bottom: 1px solid #dacbb8;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #3d362f;
  margin: 0;
  margin-bottom: 0.25rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #7d6d5f;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
}

/* ========== OVERVIEW TEXT ========== */
.overview-text {
  font-size: 1rem;
  line-height: 1.6;
  color: #3d362f;
  text-align: justify;
  margin: 0;
}

/* ========== SEARCH SECTION ========== */
.search-section {
  padding: 1.5rem;
  background: #f9f6f2;
  border-bottom: 1px solid #dacbb8;
}

.search-form {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #d8c8b0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  font-family: inherit;
}

.search-input:focus {
  outline: none;
  border-color: #8f7b65;
  box-shadow: 0 0 0 3px rgba(143, 123, 101, 0.1);
}

.search-input::placeholder {
  color: #b8a89a;
}

.btn-search {
  padding: 0.75rem 1.5rem;
  background: #8f7b65;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.3);
  background: #7a6a58;
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
  background: #fff9f1;
  border: 1px solid #e6d6c5;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.doctor-item:hover {
  background: #f7eee5;
  transform: translateX(3px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.1);
}

.doctor-info {
  flex: 1;
}

.doctor-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #3d362f;
  margin: 0 0 0.25rem 0;
}

.doctor-specialty {
  font-size: 0.9rem;
  color: #7d6d5f;
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
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.85rem;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-details {
  background: #f0e5d8;
  color: #8f7b65;
  border: 1px solid #d8c8b0;
}

.btn-details:hover {
  background: #e8dcc9;
  transform: translateY(-2px);
  border-color: #8f7b65;
}

.btn-book {
  background: #8f7b65;
  color: white;
  border: none;
}

.btn-book:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.3);
  background: #7a6a58;
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 3rem 2rem;
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

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #6d5f53;
  font-style: italic;
  background: #fff7f0;
  border-radius: 16px;
  border: 1px dashed #d7c7b5;
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
  background: #fffdf7;
  border-radius: 24px;
  border: 1px solid #d8c8b0;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 500px;
  animation: slideUp 0.3s ease-out;
  z-index: 1001;
  position: relative;
  overflow: hidden;
}

.modal-header {
  padding: 1.5rem;
  background: #f4e9db;
  color: #3d362f;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #dacbb8;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 800;
}

.modal-close {
  background: none;
  border: none;
  color: #8f7b65;
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
  color: #3d362f;
}

.modal-body {
  padding: 2rem;
}

.detail-group {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem 0;
  border-bottom: 1px solid #dacbb8;
}

.detail-group:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 800;
  color: #3d362f;
  min-width: 120px;
}

.detail-value {
  color: #7d6d5f;
  text-align: right;
  flex: 1;
}

.empty-modal-state {
  text-align: center;
  padding: 2rem;
  color: #6d5f53;
  font-style: italic;
  background: #fff7f0;
  border-radius: 16px;
  border: 1px dashed #d7c7b5;
}

.availability-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.availability-item {
  padding: 1rem;
  background: #fff9f1;
  border-radius: 12px;
  border-left: 4px solid #8f7b65;
  border: 1px solid #e6d6c5;
}

.availability-date {
  font-weight: 800;
  color: #3d362f;
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
  border-radius: 999px;
  font-weight: 700;
  font-size: 0.8rem;
}

.status-badge.bg-success {
  background: rgba(85, 158, 104, 0.15);
  color: #3d5f3d;
  border: 1px solid #559e68;
}

.status-badge.bg-danger {
  background: rgba(138, 47, 42, 0.15);
  color: #5c3d3d;
  border: 1px solid #8a5a5a;
}

.status-badge.bg-info {
  background: rgba(143, 123, 101, 0.15);
  color: #3d362f;
  border: 1px solid #d8c8b0;
}

.time-slot {
  color: #7d6d5f;
  font-size: 0.9rem;
}

.modal-footer {
  padding: 1rem 2rem;
  background: #f9f6f2;
  border-top: 1px solid #dacbb8;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-modal-close {
  padding: 0.6rem 1.5rem;
  background: #8f7b65;
  color: white;
  border: none;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s ease;
}

.btn-modal-close:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.3);
  background: #7a6a58;
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