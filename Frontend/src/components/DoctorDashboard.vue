<template>
  <div class="bg-light min-vh-100">
    <div class="bg-primary text-white py-4">
      <div class="container-fluid">
        <h1 class="text-center mb-0">Doctors' Dashboard</h1>
      </div>
    </div>

    <DoctorNavBar />

    <div class="container-fluid py-4">
      <div class="row g-4">
        <div class="col-lg-8">
          <div class="card shadow">
            <div class="card-header">
              <h2 class="card-title mb-0">Upcoming Appointments</h2>
            </div>
            <div class="card-body">
              <div v-if="appointments.length === 0" class="text-center text-muted py-4">
                No upcoming appointments
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Sr No.</th>
                      <th>Patient Name</th>
                      <th>Patient History</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(a, idx) in appointments" :key="a.id">
                      <td>{{ idx + 1 }}</td>
                      <td>{{ a.patient_name }}</td>
                      <td>
                        <button class="btn btn-outline-primary btn-sm" @click="updateHistory(a.id)">Update</button>
                      </td>
                      <td>
                        <div class="btn-group" role="group">
                          <button class="btn btn-success btn-sm" @click="markComplete(a.id)">Mark Complete</button>
                          <button class="btn btn-danger btn-sm" @click="cancelAppointment(a.id)">Cancel</button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card shadow mb-4">
            <div class="card-header">
              <h2 class="card-title mb-0">Assigned Patients</h2>
            </div>
            <div class="card-body">
              <div v-if="patients.length === 0" class="text-center text-muted py-4">
                No assigned patients
              </div>
              <div v-else>
                <div v-for="p in patients" :key="p.id" class="d-flex justify-content-between align-items-center border rounded p-2 mb-2">
                  <span class="fw-bold">{{ p.name }}</span>
                  <button class="btn btn-outline-secondary btn-sm" @click="viewPatient(p.id)">View</button>
                </div>
              </div>
            </div>
          </div>

          <div class="card shadow">
            <div class="card-body text-center">
              <button class="btn btn-success w-100" @click="provideAvailability">Provide Availability</button>
            </div>
          </div>
        </div>
      </div>
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
