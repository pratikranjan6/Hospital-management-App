<template>
  <div class="doctor-availability">
    <h2>Doctor's Availability</h2>

    <div class="availability-list">
      <div v-if="loading" class="loading">Loading...</div>
      <div v-else-if="availabilities.length === 0" class="no-data">No availability found</div>
        

        
      <div v-for="item in availabilities" :key="item.id" class="avail-row">
        <div class="date-box">{{ formatDate(item.date) }}</div>
        <button
          class="slot-box"
          :class="{'available': isAvailable(item), 'not-available': !isAvailable(item)}"
          @click="toggle(item)"
        >
          <div class="times">{{ item.start_time ? item.start_time : defaultStart }} - {{ item.end_time ? item.end_time : defaultEnd }}</div>
          <div class="status">{{ isAvailable(item) ? 'Available' : 'Not Available' }}</div>
        </button>
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

<style scoped>
.doctor-availability { padding: 18px; font-family: Inter, Arial, sans-serif }
.doctor-availability h2 { margin: 0 0 12px 0 ;color:black;}
.availability-list { display:flex; flex-direction:column; gap:10px }
.avail-row { display:flex; gap:12px; align-items:center }
.date-box { min-width:140px; padding:10px 12px; background:#eef2ff;color:black; border:2px solid #c7ddff; border-radius:6px; text-align:center; font-weight:600 }
.slot-box { display:flex; flex-direction:column; align-items:center; padding:10px 16px; border-radius:8px; cursor:pointer; border:3px solid transparent; background:#fff; min-width:220px }
.slot-box.available { border-color:#06b6a4; background:#ecfdf5 }
.slot-box.not-available { border-color:#ef4444; background:#fff7f7 }
.slot-box .times { font-weight:700; color:#0f1724 }
.slot-box .status { font-size:12px; color:#334155; margin-top:6px }
.loading, .no-data { padding:12px; color:#64748b }

@media (max-width:700px) {
  .avail-row { flex-direction:column; align-items:stretch }
  .date-box { width:100% }
  .slot-box { width:100% }
}
</style>
