<template>
  <div class="admin-wrapper">
    <DoctorNavBar />
    
    <div class="admin-container">
      <div class="availability-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title"> Doctor's Availability</h2>
            <p class="card-subtitle">Manage your availability schedule</p>
          </div>
        </div>
        
        <div class="card-body">
          <!-- Loading State -->
          <div v-if="loading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading availability...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="availabilities.length === 0" class="empty-state">
            <p>📭 No availability schedule found</p>
          </div>

          <!-- Availability Grid -->
          <div v-else class="availability-grid">
            <div v-for="item in availabilities" :key="item.id" class="availability-item">
              <div class="item-header">
                <span class="date-badge">{{ formatDate(item.date) }}</span>
              </div>
              <div class="item-body">
                <div class="time-slot">
                  <span class="label">Time:</span>
                  <span class="value">
                    {{ item.start_time ? item.start_time : defaultStart }} - 
                    {{ item.end_time ? item.end_time : defaultEnd }}
                  </span>
                </div>
                <div class="status-badge" :class="{ 'available': isAvailable(item), 'unavailable': !isAvailable(item) }">
                  {{ isAvailable(item) ? ' Available' : ' Not Available' }}
                </div>
              </div>
              <div class="item-footer">
                <button
                  class="toggle-btn"
                  :class="{ 'active': isAvailable(item) }"
                  @click="toggle(item)"
                  :title="isAvailable(item) ? 'Mark as unavailable' : 'Mark as available'"
                >
                  {{ isAvailable(item) ? 'Make Unavailable' : 'Make Available' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Back Button -->
          <div class="button-group">
            <button @click="goBack" class="btn-back">← Back to Dashboard</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAuthHeader } from '../utils/auth.js'
import { getApiBase } from '../utils/auth.js'
import DoctorNavBar from './DoctorNavBar.vue'

export default {
  name: 'DoctorAvailability',
  components: {
    DoctorNavBar
  },
  data() {
    return {
      availabilities: [],
      loading: true,
      defaultStart: '09:00',
      defaultEnd: '17:00',
      doctorId: null
    }
  },
  methods: {
    getAuthHeader,
    async fetchCurrentDoctorId() {
      try {
        const token = localStorage.getItem('token')
        if (token) {
          const parts = token.split('.')
          if (parts.length === 3) {
            const payload = JSON.parse(atob(parts[1]))
            console.log('JWT payload:', payload)
            if (payload && payload.sub) {
              const id = parseInt(payload.sub, 10)
              if (!isNaN(id)) {
                console.log('Found doctor id from token:', id)
                return id
              }
            }
          }
        }
      } catch (ex) {
        console.warn('Error decoding token:', ex)
      }

      try {
        const headers = { ...this.getAuthHeader() }
        const res = await fetch('/api/login', { headers })
        console.log('login_get status:', res.status)
        if (!res.ok) return null
        const j = await res.json()
        console.log('login_get response:', j)
        if (j && j.user && j.role === 'doctor') return j.user.id
      } catch (e) {
        console.error('fetchCurrentDoctorId error:', e)
      }
      return null
    },
    formatDate(d) {
      if (!d) return ''
      const dt = new Date(d)
      const day = String(dt.getDate()).padStart(2, '0')
      const mon = String(dt.getMonth() + 1).padStart(2, '0')
      const yr = dt.getFullYear()
      return `${day}/${mon}/${yr}`
    },
    isAvailable(item) {
      return item.status && item.status.toLowerCase() === 'available'
    },
    async fetchAvailability() {
      this.loading = true
      try {
        let id = this.doctorId || (await this.fetchCurrentDoctorId())
        if (!id) {
          const params = new URLSearchParams(window.location.search)
          id = params.get('doctor') || params.get('doctorId')
        }
        if (!id) {
          this.availabilities = []
          this.loading = false
          return
        }

        const res = await fetch(`${getApiBase()}/api/doctor/${id}/availability`, { headers: { ...this.getAuthHeader() } })
        console.log('Response status:', res.status)
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        console.log('Fetched availability data:', data)
        data.sort((a,b) => new Date(a.date) - new Date(b.date))
        this.availabilities = data
      } catch (e) {
        console.error('fetchAvailability error:', e)
        this.availabilities = []
      } finally {
        this.loading = false
      }
    },
    async toggle(item) {
      const prev = item.status
      try {
        const res = await fetch(`${getApiBase()}/api/doctor/availability/${item.id}`, {
          method: 'PUT',
          headers: { 
            'Content-Type': 'application/json',
            ...this.getAuthHeader()
          },
          body: JSON.stringify({})
        })
        if (!res.ok) throw new Error('Failed')
        const j = await res.json()
        item.status = j.status || (item.status && item.status === 'Available' ? 'Not Available' : 'Available')
      } catch (e) {
        item.status = prev
        console.error('toggle error', e)
        alert('Failed to update availability')
      }
    },
    goBack() {
      this.$router.push('/doctor_dashboard')
    }
  },
  mounted() {
    const params = new URLSearchParams(window.location.search)
    const did = params.get('doctorId') || params.get('doctor')
    if (did) this.doctorId = did
    this.fetchAvailability()
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.admin-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.admin-container {
  flex: 1;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* ========== AVAILABILITY CARD ========== */
.availability-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  animation: slideUp 0.5s ease-out;
  border-top: 4px solid #1dd1a1;
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

.card-header {
  padding: 2rem;
  background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%);
  color: white;
}

.header-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.card-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin: 0;
}

.card-body {
  padding: 2rem;
}

/* ========== LOADING STATE ========== */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e0e6ed;
  border-top-color: #1dd1a1;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #7f8c8d;
  font-size: 0.95rem;
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

/* ========== AVAILABILITY GRID ========== */
.availability-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.availability-item {
  background: #f9f9f9;
  border-radius: 10px;
  border: 2px solid #e0e6ed;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.availability-item:hover {
  border-color: #1dd1a1;
  box-shadow: 0 4px 12px rgba(29, 209, 161, 0.15);
  transform: translateY(-3px);
}

.item-header {
  padding: 1rem;
  background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%);
  color: white;
}

.date-badge {
  font-size: 0.9rem;
  font-weight: 600;
}

.item-body {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.time-slot {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.75rem;
  align-items: center;
}

.time-slot .label {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.85rem;
}

.time-slot .value {
  color: #667eea;
  font-weight: 500;
  font-size: 0.95rem;
}

.status-badge {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  text-align: center;
  transition: all 0.3s ease;
}

.status-badge.available {
  background: #d4f8e8;
  color: #0d7657;
}

.status-badge.unavailable {
  background: #f8d7da;
  color: #842029;
}

.item-footer {
  padding: 0 1rem 1rem;
}

.toggle-btn {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #1dd1a1;
  background: white;
  color: #1dd1a1;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.toggle-btn:hover {
  background: #f0fdf4;
  transform: translateY(-2px);
}

.toggle-btn.active {
  background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%);
  color: white;
  border-color: #1dd1a1;
}

.toggle-btn.active:hover {
  box-shadow: 0 4px 12px rgba(29, 209, 161, 0.3);
}

/* ========== BUTTONS ========== */
.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn-back {
  padding: 0.85rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-back:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-back:active {
  transform: translateY(0);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .admin-container {
    padding: 1rem;
  }

  .card-header {
    padding: 1.5rem;
  }

  .card-body {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.4rem;
  }

  .card-subtitle {
    font-size: 0.85rem;
  }

  .availability-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .item-body {
    padding: 0.75rem;
  }

  .button-group {
    flex-direction: column;
  }

  .btn-back {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .admin-container {
    padding: 0.75rem;
  }

  .card-header {
    padding: 1rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 1.2rem;
  }

  .date-badge {
    font-size: 0.85rem;
  }

  .time-slot .label,
  .time-slot .value {
    font-size: 0.85rem;
  }

  .toggle-btn {
    padding: 0.6rem 0.8rem;
    font-size: 0.85rem;
  }

  .btn-back {
    padding: 0.7rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
