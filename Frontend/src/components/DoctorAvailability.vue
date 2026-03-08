<template>
  <div class="container-fluid bg-light min-vh-100 py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow">
          <div class="card-header">
            <h2 class="card-title mb-0">Doctor's Availability</h2>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2 text-muted">Loading availability...</p>
            </div>
            <div v-else-if="availabilities.length === 0" class="text-center text-muted py-4">
              No availability found
            </div>
            <div v-else class="row g-3">
              <div v-for="item in availabilities" :key="item.id" class="col-md-6 col-lg-4">
                <div class="card h-100">
                  <div class="card-body text-center">
                    <div class="badge bg-primary mb-3 fs-6">{{ formatDate(item.date) }}</div>
                    <button
                      class="btn w-100"
                      :class="isAvailable(item) ? 'btn-success' : 'btn-outline-danger'"
                      @click="toggle(item)"
                    >
                      <div class="fw-bold">{{ item.start_time ? item.start_time : defaultStart }} - {{ item.end_time ? item.end_time : defaultEnd }}</div>
                      <small class="text-muted">{{ isAvailable(item) ? 'Available' : 'Not Available' }}</small>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button @click="this.$router.push('/doctor_dashboard')" class="btn btn-secondary w-100 mt-3">Back</button>
        </div>
      </div>
      
    </div>

  </div>
</template>

<script>
import { getAuthHeader } from '../utils/auth.js'
import { getApiBase } from '../utils/auth.js'
export default {
  name: 'DoctorAvailability',
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
