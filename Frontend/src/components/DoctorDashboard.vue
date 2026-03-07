<template>
  <div class="doctor-dashboard">
    <header class="dd-header">
      <h1>Doctors' Dashboard</h1>
    </header>

    <DoctorNavBar />

    <div class="dd-container">

      <section class="appointments">
        <h2>Upcoming Appointments</h2>
        <div class="appt-table">
          <div class="appt-row appt-head">
            <div class="col sr">Sr No.</div>
            <div class="col name">Patient Name</div>
            <div class="col history">Patient History</div>
            <div class="col actions">Actions</div>
          </div>

          <div v-if="appointments.length === 0" class="no-data">No upcoming appointments</div>

          <div v-for="(a, idx) in appointments" :key="a.id" class="appt-row">
            <div class="col sr">{{ idx + 1 }}.</div>
            <div class="col name">{{ a.patient_name }}</div>
            <div class="col history">
              <button class="btn btn-outline" @click="updateHistory(a.id)">update</button>
            </div>
            <div class="col actions">
              <button class="btn btn-success" @click="markComplete(a.id)">mark as complete</button>
              <button class="btn btn-danger" @click="cancelAppointment(a.id)">cancel</button>
            </div>
          </div>
        </div>
      </section>

      <section class="assigned">
        <h2>Assigned Patients</h2>
        <div class="patient-list">
          <div v-if="patients.length === 0" class="no-data">No assigned patients</div>
          <div v-for="p in patients" :key="p.id" class="patient-item">
            <div class="patient-name">{{ p.name }}</div>
            <button class="btn btn-outline" @click="viewPatient(p.id)">view</button>
          </div>
        </div>

        <div class="availability">
          <button class="btn btn-success large" @click="provideAvailability">Provide Availability</button>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import DoctorNavBar from './DoctorNavBar.vue'
import { getApiBase, getAuthHeader } from '../utils/auth.js'

export default {
  name: 'DoctorDashboard',
  components: { DoctorNavBar },
  data() {
    return {
      doctorName: 'Abcde',
      appointments: [],
      patients: []
    }
  },
  methods: {
    fetchData() {
      const username = localStorage.getItem('username')
      const q = username ? `?username=${encodeURIComponent(username)}` : ''
      const headers = { ...getAuthHeader() }

      fetch(`${getApiBase()}/api/doctor/appointments${q}`, { headers })
        .then(r => r.ok ? r.json() : Promise.reject(r))
        .then(data => { this.appointments = (data || []).filter(a => a.status === 'Booked') })
        .catch(() => { this.appointments = [] })

      fetch(`${getApiBase()}/api/doctor/patients${q}`, { headers })
        .then(r => r.ok ? r.json() : Promise.reject(r))
        .then(data => { this.patients = data || [] })
        .catch(() => { this.patients = [] })
    },
    updateHistory(appointmentId) {
      if (this.$router) {
        this.$router.push({ name: 'editPatient', params: { appointmentId } })
      }
    },
    async markComplete(appointmentId) {
      if (!confirm('Mark appointment complete?')) return
      try {
        const headers = { ...getAuthHeader(), 'Content-Type': 'application/json' }
        const res = await fetch(`${getApiBase()}/api/doctor/appointment/${appointmentId}/complete`, {
          method: 'POST',
          headers
        })
        if (!res.ok) {
          const j = await res.json().catch(() => ({}))
          throw new Error(j.msg || 'Failed to mark complete')
        }
        this.$toast?.success?.('Appointment marked complete')
        this.appointments = this.appointments.filter(a => a.id !== appointmentId)
      } catch (e) {
        console.error('Error marking complete', e)
        this.$toast?.error?.(e.message || 'Failed to mark appointment complete')
      }
    },
    async cancelAppointment(appointmentId) {
      if (!confirm('Cancel appointment?')) return
      try {
        const headers = { ...getAuthHeader(), 'Content-Type': 'application/json' }
        const res = await fetch(`${getApiBase()}/api/doctor/appointment/${appointmentId}/cancel`, {
          method: 'POST',
          headers
        })
        if (!res.ok) {
          const j = await res.json().catch(() => ({}))
          throw new Error(j.msg || 'Failed to cancel')
        }
        this.$toast?.success?.('Appointment cancelled')
        this.appointments = this.appointments.filter(a => a.id !== appointmentId)
      } catch (e) {
        console.error('Error cancelling', e)
        this.$toast?.error?.(e.message || 'Failed to cancel appointment')
      }
    },

    viewPatient(patientId) {
      if (this.$router) {
        this.$router.push({ path: '/doctor_patient_history', query: { patient_id: patientId } })
      }
    },
    provideAvailability() {
      if (this.$router) {
        this.$router.push('/doctor_availability')
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      this.$router && this.$router.push('/login')
    }
  },
  mounted() {
    const storedName = localStorage.getItem('username')
    if (storedName) this.doctorName = storedName
    this.fetchData()
  }
}
</script>

<style scoped>
.doctor-dashboard { width: 100%;font-family: Inter, Arial, Helvetica, sans-serif; color: #1f2d3d; background: #f5f7fb; min-height: 100vh; display:flex; flex-direction:column; }
.dd-container { width: 100%; flex: 1 1 auto; margin: 0; background: #fff; border-radius: 0; box-shadow: none; overflow: auto; padding: 0; }

/* Navbar */
.doctor-nav { display:flex; justify-content:space-between; align-items:center; background:#0f1724; color:#fff; padding:12px 6%; }
.doctor-nav .nav-left { font-weight:600; font-size:16px }
.doctor-nav .nav-right .logout { background:transparent; border:1px solid rgba(255,255,255,0.12); color:#fff; padding:8px 12px; border-radius:6px; cursor:pointer }
.doctor-nav .nav-right .logout:hover { background:rgba(255,255,255,0.04) }

/* Header */
.dd-header { text-align: center; padding: 24px 16px; border-bottom: 1px solid #eef2f6; }
.dd-header h1 { margin: 0; font-weight: 700; font-size: 28px; color: #0f1724 }

/* Topbar */
.dd-topbar { display:flex; justify-content:space-between; align-items:center; padding:14px 18px; background:#ffffff; }
.welcome { font-size:18px; font-weight:600; color:#0f1724 }
.logout { background:transparent; border:1px solid #e2e8f0; padding:8px 12px; border-radius:6px; color:#0f1724; cursor:pointer }
.logout:hover { background:#f8fafc }

/* Sections */
.content { display:flex; gap:18px; padding:18px }
.appointments, .assigned { padding:18px; background: transparent }

/* Make sections share space */
.appointments { flex: 2 }
.assigned { flex: 1 }
.appointments h2, .assigned h2 { margin:0 0 12px 0; font-size:18px; color:#102a43 }

/* Appointment rows as grid for consistent columns */
.appt-table { border:1px solid #e6eef6; border-radius:6px; overflow:hidden }
.appt-row { display:grid; grid-template-columns: 64px 1fr 220px 240px; gap:12px; align-items:center; padding:12px 16px; border-bottom:1px solid #f1f5f9 }
.appt-row:last-child { border-bottom:none }
.appt-head { background:#f8fafc; font-weight:700; color:#0f1724 }
.col { padding:0 }
.col.sr { color:#475569; font-weight:600 }
.col.name { color:#0f1724 }
.col.actions { display:flex; gap:10px; justify-self:start }

.no-data { padding:12px 16px; color:#64748b }

/* Patients list */
.patient-list { border:1px solid #e6eef6; border-radius:6px; padding:8px }
.patient-item { display:flex; justify-content:space-between; align-items:center; padding:10px 12px; background:#fbfdff; border-radius:6px; margin-bottom:8px; border:1px solid #f1f5f9 }
.patient-item:last-child { margin-bottom:0 }
.patient-name { color:#334155; font-weight:600 }

/* Buttons */
.btn { padding:8px 14px; border-radius:8px; cursor:pointer; border:1px solid transparent; font-weight:600; font-size:14px }
.btn-outline { background:#fff; border:2px solid #3b82f6; color:#0f1724 }
.btn-outline:hover { background:#eff6ff }
.btn-success { background:#10b981; color:white; border:1px solid rgba(16,185,129,0.15) }
.btn-success:hover { opacity:0.95 }
.btn-danger { background:#ef4444; color:white }
.btn-danger:hover { opacity:0.95 }
.large { padding:10px 18px }

/* Availability button alignment */
.availability { margin-top:12px; text-align:right }

/* Responsive adjustments */
@media (max-width: 1100px) {
  .content { flex-direction:column }
  .appt-row { grid-template-columns: 48px 1fr; grid-auto-rows: auto }
  .col.history { order: 3; }
  .col.actions { order: 4; justify-self:end; width: auto }
  .col.actions button { margin-left:6px }
}

</style>
