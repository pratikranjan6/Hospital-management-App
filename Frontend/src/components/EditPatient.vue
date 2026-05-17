<template>
  <div class="container-fluid bg-light min-vh-100 py-5">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card shadow" style="background: #fffdf7;">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h1 class="h4 mb-0" style="color: #3d362f;">Update Patient History</h1>
            <button @click="goBack" class="btn btn-outline-secondary" style="color: #8f7b65;">
              <i class="bi bi-arrow-left"></i> Back
            </button>
          </div>
          <div class="card-body">
            <div v-if="loading" class="text-center py-4" style="background: #fff9f1; border-radius: 16px; padding: 2rem;">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2 text-muted" style="color: #7d6d5f;">Loading appointment data...</p>
            </div>
            <form v-else @submit.prevent="submitHistory">
              <div class="row mb-3">
                <div class="col-md-4">
                  <label class="form-label fw-bold" style="color: #3d362f;">Appointment ID:</label>
                  <p class="mb-0" style="color: #8f7b65; font-weight: 600;">{{ appointmentId }}</p>
                </div>
                <div class="col-md-4" v-if="appointment.patient_name">
                  <label class="form-label fw-bold" style="color: #3d362f;">Patient:</label>
                  <p class="mb-0" style="color: #8f7b65; font-weight: 600;">{{ appointment.patient_name }}</p>
                </div>
                <div class="col-md-4" v-if="appointment.doctor_name">
                  <label class="form-label fw-bold" style="color: #3d362f;">Doctor:</label>
                  <p class="mb-0" style="color: #8f7b65; font-weight: 600;">{{ appointment.doctor_name }}</p>
                </div>
              </div>

              <div class="mb-3">
                <label for="tests" class="form-label" style="color: #3d362f;">Tests Done</label>
                <input id="tests" v-model="form.tests_done" type="text" class="form-control" placeholder="e.g. ECG, Blood test" style="background: #fff9f1; border: 1px solid #d8c8b0; color: #3d362f; border-radius: 16px;" />
              </div>

              <div class="mb-3">
                <label for="diagnosis" class="form-label" style="color: #3d362f;">Diagnosis</label>
                <input id="diagnosis" v-model="form.diagnosis" type="text" class="form-control" placeholder="e.g. Hypertension" style="background: #fff9f1; border: 1px solid #d8c8b0; color: #3d362f; border-radius: 16px;" />
              </div>

              <div class="mb-3">
                <label for="prescription" class="form-label" style="color: #3d362f;">Prescription</label>
                <input id="prescription" v-model="form.prescription" type="text" class="form-control" placeholder="e.g. Apply ointment twice daily" style="background: #fff9f1; border: 1px solid #d8c8b0; color: #3d362f; border-radius: 16px;" />
              </div>

              <div class="mb-3">
                <label for="medicines" class="form-label" style="color: #3d362f;">Medicines (comma separated)</label>
                <input id="medicines" v-model="form.medicines" type="text" class="form-control" placeholder="e.g. Paracetamol, Ibuprofen" style="background: #fff9f1; border: 1px solid #d8c8b0; color: #3d362f; border-radius: 16px;" />
              </div>

              <div class="text-end">
                <button type="submit" class="btn btn-success" :disabled="saving" style="background: #8f7b65; border-color: #8f7b65; color: white; font-weight: 700; border-radius: 999px; padding: 0.85rem 2rem;">
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
      <div class="toast show" :style="messageType === 'success' ? 'background: #8f7b65 !important;' : 'background: #c85a5a !important;'" style="border-radius: 16px;" role="alert">
        <div class="toast-body text-white d-flex justify-content-between align-items-center" style="color: white !important; font-weight: 500;">
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
/* ========== MAIN CONTAINER ========== */
.container-fluid.bg-light {
  background: #f2e8d8 !important;
}

/* ========== CARD ========== */
.card {
  background: #fffdf7;
  border: 1px solid #d8c8b0;
  border-radius: 24px;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
}

.card-header {
  background: #f4e9db;
  color: #3d362f;
  border-bottom: 1px solid #dacbb8;
  border-radius: 24px 24px 0 0;
  font-weight: 700;
}

.card-header .h4 {
  color: #3d362f;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.card-header .btn-outline-secondary {
  border-color: #d8c8b0;
  color: #8f7b65;
  background: transparent;
  font-weight: 600;
}

.card-header .btn-outline-secondary:hover {
  background-color: #8f7b65;
  border-color: #8f7b65;
  color: white;
}

/* ========== FORM LABELS ========== */
.form-label {
  color: #3d362f;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

p:not(.mt-2) {
  color: #7d6d5f;
}

/* ========== FORM CONTROLS ========== */
.form-control {
  background: #fff9f1;
  border: 1px solid #d8c8b0;
  color: #3d362f;
  border-radius: 16px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  background: #fffdf7;
  border-color: #8f7b65;
  color: #3d362f;
  box-shadow: 0 0 0 0.2rem rgba(143, 123, 101, 0.15);
}

.form-control::placeholder {
  color: #bfafa1;
}

/* ========== BUTTONS ========== */
.btn-success {
  background: #8f7b65;
  border-color: #8f7b65;
  color: white;
  font-weight: 700;
  border-radius: 999px;
  padding: 0.85rem 2rem;
  transition: all 0.3s ease;
}

.btn-success:hover {
  background: #7a6a58;
  border-color: #7a6a58;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(143, 123, 101, 0.3);
}

.btn-success:disabled {
  background: #bfafa1;
  border-color: #bfafa1;
  opacity: 0.7;
}

/* ========== SPINNER ========== */
.spinner-border {
  color: #8f7b65 !important;
  border: 0.35em solid #d8c8b0 !important;
  border-right-color: #8f7b65 !important;
}

.spinner-border-sm {
  color: white !important;
}

.text-muted {
  color: #7d6d5f !important;
}

.text-primary {
  color: #8f7b65 !important;
}

/* ========== TOAST ========== */
.toast.bg-success {
  background: #8f7b65 !important;
}

.toast.bg-danger {
  background: #c85a5a !important;
}

.toast-body {
  font-weight: 500;
}
</style>