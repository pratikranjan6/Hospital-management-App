<template>
  <div class="edit-patient">
    <div class="header">
      <h1>Update Patient History</h1>
      <button @click="goBack" class="back-btn">← Back</button>
    </div>

    <div v-if="loading" class="loading">Loading appointment data...</div>
    <div v-else>
      <form @submit.prevent="submitHistory" class="history-form">
        <div class="form-group">
          <label>Appointment ID:</label>
          <span>{{ appointmentId }}</span>
        </div>
        <div class="form-group" v-if="appointment.patient_name">
          <label>Patient:</label>
          <span>{{ appointment.patient_name }}</span>
        </div>
        <div class="form-group" v-if="appointment.doctor_name">
          <label>Doctor:</label>
          <span>{{ appointment.doctor_name }}</span>
        </div>

        <div class="form-group">
          <label for="tests">Tests Done</label>
          <input id="tests" v-model="form.tests_done" type="text" placeholder="e.g. ECG, Blood test" />
        </div>

        <div class="form-group">
          <label for="diagnosis">Diagnosis</label>
          <input id="diagnosis" v-model="form.diagnosis" type="text" placeholder="e.g. Hypertension" />
        </div>

        <div class="form-group">
          <label for="prescription">Prescription</label>
          <input id="prescription" v-model="form.prescription" type="text" placeholder="e.g. Apply ointment twice daily" />
        </div>

        <div class="form-group">
          <label for="medicines">Medicines (comma separated)</label>
          <input id="medicines" v-model="form.medicines" type="text" placeholder="e.g. Paracetamol, Ibuprofen" />
        </div>

        <div class="form-actions">
          <button type="submit" class="save-btn" :disabled="saving">
            {{ saving ? 'Saving...' : 'Update History' }}
          </button>
        </div>
      </form>
    </div>

    <div v-if="message" class="message" :class="messageType">
      {{ message }}
      <button class="close-msg" @click="message = ''">×</button>
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
.edit-patient {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  font-family: Arial, sans-serif;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}
.back-btn {
  background: #ccc;
  border: none;
  padding: 8px 14px;
  border-radius: 4px;
  cursor: pointer;
}
.loading {
  text-align: center;
  color: #666;
}
.history-form .form-group {
  margin-bottom: 20px;
}
.history-form label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
}
.history-form input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-actions {
  text-align: right;
}
.save-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 4px;
  cursor: pointer;
}
.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 4px;
  color: white;
  display: flex;
  align-items: center;
  gap: 12px;
}
.message.success { background: #4CAF50; }
.message.error { background: #f44336; }
.close-msg {
  background: transparent;
  border: none;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  color: white;
}
</style>