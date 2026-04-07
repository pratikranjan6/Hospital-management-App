<template>
  <div class="history-wrapper">
    <div class="history-container">
      <!-- Welcome Header -->
      <div class="welcome-section">
        <div class="welcome-content">
          <div>
            <h1 class="welcome-title">
              <i class="fas fa-history"></i> My Medical History
            </h1>
            <p class="welcome-subtitle">Your complete medical appointment and visit records</p>
          </div>
          <div class="header-actions">
            <router-link to="/user_dashboard" class="nav-link-btn">
              <i class="fas fa-home"></i> Dashboard
            </router-link>
            <button @click="exportHistory" class="nav-link-btn export-btn">
              <i class="fas fa-download"></i> Export CSV
            </button>
            <button @click="logout" class="nav-link-btn logout-btn">
              <i class="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
        </div>
      </div>

      <!-- Patient Information Card -->
      <div class="info-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title">
              <i class="fas fa-user-circle"></i> Patient Information
            </h2>
          </div>
        </div>
        <div class="card-body">
          <div class="patient-info">
            <div class="info-item">
              <span class="info-label">
                <i class="fas fa-user"></i> Patient Name
              </span>
              <span class="info-value">{{ patientName }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Visit History Card -->
      <div class="history-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title">
              <i class="fas fa-calendar-check"></i> Visit History
            </h2>
            <p class="card-subtitle">{{ visits.length }} visits recorded</p>
          </div>
        </div>

        <div class="card-body">
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading medical history...</p>
          </div>

          <div v-else-if="visits.length === 0" class="empty-state">
            <i class="fas fa-inbox"></i>
            <p>No visit history found</p>
            <router-link to="/user_dashboard" class="btn-empty">Book Your First Appointment</router-link>
          </div>

          <div v-else class="visits-table-wrapper">
            <div class="visits-table">
              <div class="table-header">
                <div class="col-no">SR</div>
                <div class="col-doctor">Doctor</div>
                <div class="col-dept">Department</div>
                <div class="col-date">Date</div>
                <div class="col-tests">Tests</div>
                <div class="col-diagnosis">Diagnosis</div>
                <div class="col-prescription">Prescription</div>
                <div class="col-medicines">Medicines</div>
              </div>

              <div v-for="(visit, index) in visits" :key="visit.id" class="table-row">
                <div class="col-no">{{ index + 1 }}</div>
                <div class="col-doctor">
                  <div class="doctor-badge">Dr. {{ visit.doctor_name || 'N/A' }}</div>
                </div>
                <div class="col-dept">{{ visit.department || 'N/A' }}</div>
                <div class="col-date">
                  <span class="date-badge">{{ formatDate(visit.date) }}</span>
                </div>
                <div class="col-tests">{{ visit.tests_done || 'N/A' }}</div>
                <div class="col-diagnosis">{{ visit.diagnosis || 'N/A' }}</div>
                <div class="col-prescription">{{ visit.prescription || 'N/A' }}</div>
                <div class="col-medicines">
                  <div v-if="visit.medicines && visit.medicines.length > 0" class="medicines-list">
                    <span v-for="medicine in visit.medicines" :key="medicine" class="medicine-badge">
                      {{ medicine }}
                    </span>
                  </div>
                  <span v-else class="text-muted">N/A</span>
                </div>
              </div>
            </div>
          </div>

          <div class="card-footer">
            <button @click="goBack" class="btn-secondary">
              <i class="fas fa-arrow-left"></i> Go Back
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Notification -->
    <div v-if="successMessage" class="notification success-notification">
      <div class="notification-content">
        <i class="fas fa-check-circle"></i>
        <div>
          <p class="notification-title">Success</p>
          <p class="notification-message">{{ successMessage }}</p>
        </div>
      </div>
      <button class="notification-close" @click="successMessage = ''">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <!-- Error Notification -->
    <div v-if="errorMessage" class="notification error-notification">
      <div class="notification-content">
        <i class="fas fa-exclamation-circle"></i>
        <div>
          <p class="notification-title">Error</p>
          <p class="notification-message">{{ errorMessage }}</p>
        </div>
      </div>
      <button class="notification-close" @click="errorMessage = ''">
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'UserPatientHistory',
  data() {
    return {
      patientName: 'User',
      visits: [],
      loading: true,
      successMessage: '',
      errorMessage: ''
    }
  },
  mounted() {
    this.fetchUserHistory()
  },
  methods: {
    async fetchUserHistory() {
      try {
        this.loading = true
        const response = await fetch(`${getApiBase()}/api/patient/history`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to fetch history')
        }

        const data = await response.json()
        this.patientName = data.patient_name || 'User'
        this.visits = Array.isArray(data.appointments) ? data.appointments : []
      } catch (error) {
        console.error('Error fetching patient history:', error)
        this.errorMessage = 'Failed to load medical history'
      } finally {
        this.loading = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-GB')
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
        this.successMessage = 'Export started. You will receive an email when it completes.'

        const checkStatus = async () => {
          try {
            const s = await fetch(`${getApiBase()}/api/patient/export_status`, {
              method: 'GET',
              headers: getAuthHeader()
            })
            if (s.ok) {
              const data = await s.json()
              if (data.done) {
                this.successMessage = 'Export completed; check your email.'
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
        this.errorMessage = 'Failed to start export'
      }
    },

    goBack() {
      this.$router.back()
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      this.$router.push('/login')
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

.history-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.history-container {
  flex: 1;
  padding: 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
}

/* ========== ANIMATIONS ========== */
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(400px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* ========== WELCOME SECTION ========== */
.welcome-section {
  margin-bottom: 2rem;
  animation: slideDown 0.5s ease-out;
}

.welcome-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.welcome-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-title i {
  font-size: 2.5rem;
}

.welcome-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items: center;
}

.nav-link-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  white-space: nowrap;
}

.nav-link-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.export-btn {
  background: rgba(52, 211, 153, 0.2);
  border-color: rgba(52, 211, 153, 0.4);
}

.export-btn:hover {
  background: rgba(52, 211, 153, 0.3);
}

.logout-btn {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

/* ========== INFO CARD ========== */
.info-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  /* border-top: 4px solid #667eea; */
  margin-bottom: 2rem;
  animation: cardSlide 0.5s ease-out;
}

.info-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #e0e0e0;
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-title i {
  color: #667eea;
  font-size: 1.5rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0.25rem 0 0 0;
}

.card-body {
  padding: 1.5rem;
}

.patient-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-label i {
  color: #667eea;
  font-size: 1rem;
}

.info-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2c3e50;
}

/* ========== HISTORY CARD ========== */
.history-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  /* border-top: 4px solid #764ba2; */
  animation: cardSlide 0.5s ease-out 0.1s backwards;
}

.history-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
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

/* ========== EMPTY STATE ========== */
.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #7f8c8d;
}

.empty-state i {
  font-size: 3rem;
  color: #ddd;
  display: block;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.btn-empty {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-empty:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* ========== TABLE STYLES ========== */
.visits-table-wrapper {
  overflow-x: auto;
}

.visits-table {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: grid;
  grid-template-columns: 50px 1.2fr 1.2fr 100px 1fr 1.2fr 1.2fr 1.2fr;
  gap: 1rem;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  border-radius: 8px 8px 0 0;
  margin-bottom: 0.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

.table-row {
  display: grid;
  grid-template-columns: 50px 1.2fr 1.2fr 100px 1fr 1.2fr 1.2fr 1.2fr;
  gap: 1rem;
  padding: 1rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  transition: all 0.2s ease;
  align-items: center;
  font-size: 0.925rem;
  color: #2c3e50;
}

.table-row:hover {
  background: #f0f2f9;
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

/* Table Columns */
.col-no {
  font-weight: 700;
  color: #667eea;
}

.doctor-badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  background: linear-gradient(135deg, #e8eef7 0%, #f0f2f9 100%);
  color: #667eea;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
}

.date-badge {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border-radius: 6px;
  font-weight: 600;
  font-size: 0.9rem;
}

.medicines-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.medicine-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  background: linear-gradient(135deg, #fef08a 0%, #fde047 100%);
  color: #78350f;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.text-muted {
  color: #7f8c8d;
  font-style: italic;
}

/* ========== CARD FOOTER ========== */
.card-footer {
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
  background: #f9f9f9;
  text-align: right;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: white;
  color: #667eea;
  border: 1.5px solid #667eea;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-secondary:hover {
  background: #e8eef7;
  transform: translateY(-2px);
}

/* ========== NOTIFICATIONS ========== */
.notification {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  max-width: 420px;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.success-notification {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border: 1px solid #6ee7b7;
}

.error-notification {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 1px solid #fca5a5;
}

.notification-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  flex: 1;
}

.notification-content i {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.success-notification i {
  color: #10b981;
}

.error-notification i {
  color: #ef4444;
}

.notification-title {
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.success-notification .notification-title {
  color: #166534;
}

.error-notification .notification-title {
  color: #991b1b;
}

.notification-message {
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.85;
}

.success-notification .notification-message {
  color: #166534;
}

.error-notification .notification-message {
  color: #991b1b;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.success-notification .notification-close {
  color: #10b981;
}

.error-notification .notification-close {
  color: #ef4444;
}

.notification-close:hover {
  transform: scale(1.2);
}

/* ========== RESPONSIVE DESIGN ========== */
@media (max-width: 1200px) {
  .table-header,
  .table-row {
    grid-template-columns: 45px 1fr 1fr 90px 1fr 1fr 1fr 1fr;
    font-size: 0.85rem;
  }
}

@media (max-width: 968px) {
  .table-header,
  .table-row {
    grid-template-columns: 40px 1fr 0.9fr 80px 0.9fr 0.9fr 0.9fr 0.9fr;
  }

  .history-container {
    padding: 1.5rem;
  }

  .welcome-content {
    flex-direction: column;
    text-align: center;
  }

  .welcome-title {
    font-size: 1.5rem;
  }

  .header-actions {
    justify-content: center;
    width: 100%;
  }

  .patient-info {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .history-container {
    padding: 1rem;
  }

  .welcome-section {
    margin-bottom: 1.5rem;
  }

  .welcome-content {
    padding: 1.5rem;
    gap: 1rem;
  }

  .welcome-title {
    font-size: 1.3rem;
  }

  .welcome-subtitle {
    font-size: 0.85rem;
  }

  .header-actions {
    width: 100%;
  }

  .nav-link-btn {
    flex: 1;
    justify-content: center;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }

  .card-header {
    padding: 1rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .info-item {
    margin-bottom: 1rem;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
    padding: 0.75rem;
    margin-bottom: 0.75rem;
  }

  .table-header {
    display: none;
  }

  .table-row {
    display: block;
  }

  .table-row > div {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .table-row > div::before {
    content: attr(data-label);
    font-weight: 700;
    color: #667eea;
  }

  .card-footer {
    text-align: center;
  }

  .btn-secondary {
    width: 100%;
  }

  .notification {
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .history-container {
    padding: 0.75rem;
  }

  .welcome-content {
    padding: 1rem;
  }

  .welcome-title {
    font-size: 1.1rem;
    gap: 0.5rem;
  }

  .welcome-title i {
    font-size: 1.8rem;
  }

  .welcome-subtitle {
    font-size: 0.75rem;
  }

  .nav-link-btn {
    padding: 0.5rem 0.6rem;
    font-size: 0.75rem;
    gap: 0.3rem;
  }

  .card-body {
    padding: 0.75rem;
  }

  .card-title {
    font-size: 1rem;
    gap: 0.5rem;
  }

  .card-title i {
    font-size: 1.2rem;
  }

  .info-label {
    font-size: 0.75rem;
  }

  .info-value {
    font-size: 1.1rem;
  }

  .table-row {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.5rem;
    padding: 0.75rem;
    font-size: 0.85rem;
  }

  .notification {
    top: 1rem;
    right: 0.5rem;
    left: 0.5rem;
    font-size: 0.85rem;
  }

  .btn-secondary {
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
