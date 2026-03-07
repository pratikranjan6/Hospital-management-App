<template>
  <div class="container-fluid bg-light min-vh-100 py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h1 class="h4 mb-0">Update Patient History</h1>
            <button @click="goBack" class="btn btn-outline-secondary">
              <i class="bi bi-arrow-left"></i> Back
            </button>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2 text-muted">Loading appointment data...</p>
            </div>
            <form v-else @submit.prevent="submitHistory">
              <div class="row mb-3">
                <div class="col-md-4">
                  <label class="form-label fw-bold">Appointment ID:</label>
                  <p class="mb-0">{{ appointmentId }}</p>
                </div>
                <div class="col-md-4" v-if="appointment.patient_name">
                  <label class="form-label fw-bold">Patient:</label>
                  <p class="mb-0">{{ appointment.patient_name }}</p>
                </div>
                <div class="col-md-4" v-if="appointment.doctor_name">
                  <label class="form-label fw-bold">Doctor:</label>
                  <p class="mb-0">{{ appointment.doctor_name }}</p>
                </div>
              </div>

              <div class="mb-3">
                <label for="tests" class="form-label">Tests Done</label>
                <input id="tests" v-model="form.tests_done" type="text" class="form-control" placeholder="e.g. ECG, Blood test" />
              </div>

              <div class="mb-3">
                <label for="diagnosis" class="form-label">Diagnosis</label>
                <input id="diagnosis" v-model="form.diagnosis" type="text" class="form-control" placeholder="e.g. Hypertension" />
              </div>

              <div class="mb-3">
                <label for="prescription" class="form-label">Prescription</label>
                <input id="prescription" v-model="form.prescription" type="text" class="form-control" placeholder="e.g. Apply ointment twice daily" />
              </div>

              <div class="mb-3">
                <label for="medicines" class="form-label">Medicines (comma separated)</label>
                <input id="medicines" v-model="form.medicines" type="text" class="form-control" placeholder="e.g. Paracetamol, Ibuprofen" />
              </div>

              <div class="text-end">
                <button type="submit" class="btn btn-success" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status"></span>
                  {{ saving ? 'Saving...' : 'Update History' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div v-if="message" class="toast-container position-fixed top-0 end-0 p-3">
      <div class="toast show" :class="messageType === 'success' ? 'bg-success' : 'bg-danger'" role="alert">
        <div class="toast-body text-white d-flex justify-content-between align-items-center">
          {{ message }}
          <button type="button" class="btn-close btn-close-white" @click="message = ''"></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'
export default {
  name: 'EditPatient',
  data() {
    return {
      appointmentId: null,
      appointment: {},
      form: {
        tests_done: '',
        diagnosis: '',
        prescription: '',
        medicines: ''
      },
      loading: true,
      saving: false,
      message: '',
      messageType: ''
    }
  },
  mounted() {
    this.appointmentId = this.$route.params.appointmentId
    if (this.appointmentId) {
      this.fetchAppointment()
    } else {
      this.loading = false
      this.message = 'Invalid appointment';
      this.messageType = 'error'
    }
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    async fetchAppointment() {
      try {
        this.loading = true
        const res = await fetch(`${getApiBase()}/api/appointment/${this.appointmentId}`, {
          headers: getAuthHeader()
        })
        if (!res.ok) {
          throw new Error('Failed to load appointment')
        }
        const data = await res.json()
        this.appointment = data
        this.form.tests_done = data.tests_done || ''
        this.form.diagnosis = data.diagnosis || ''
        this.form.prescription = data.prescription || ''
        this.form.medicines = data.medicines || ''
      } catch (e) {
        console.error(e)
        this.message = e.message || 'Error loading appointment data'
        this.messageType = 'error'
      } finally {
        this.loading = false
      }
    },
    async submitHistory() {
      try {
        this.saving = true
        const body = {
          tests_done: this.form.tests_done,
          diagnosis: this.form.diagnosis,
          prescription: this.form.prescription,
          medicines: this.form.medicines
        }
        const res = await fetch(`${getApiBase()}/api/appointment/${this.appointmentId}/history`, {
          method: 'PUT',
          headers: {
            ...getAuthHeader(),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(body)
        })
        if (!res.ok) {
          const j = await res.json().catch(() => ({}))
          throw new Error(j.msg || 'Failed to update history')
        }
        this.message = 'History updated successfully'
        this.messageType = 'success'
      } catch (e) {
        console.error(e)
        this.message = e.message || 'Failed to update history'
        this.messageType = 'error'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.card-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom: none;
}

.card-header .btn-outline-secondary {
  border-color: rgba(255, 255, 255, 0.5);
  color: white;
}

.card-header .btn-outline-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: white;
  color: white;
}
</style>