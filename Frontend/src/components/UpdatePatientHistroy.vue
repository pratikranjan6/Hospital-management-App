<template>
  <div class="container-fluid mt-5">
    <div class="card">
      <div class="card-header bg-primary text-white">
        <h2 class="h4 mb-0">Update Patient History</h2>
      </div>
      <div class="card-body">
        <div class="mb-3">
          <strong>Patient Name:</strong> {{ patientName }}
        </div>
        <div class="mb-3">
          <strong>Department:</strong> {{ department || 'N/A' }}
        </div>

        <form @submit.prevent="saveHistory">
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Visit Type</label>
              <input v-model="form.visit_type" class="form-control" placeholder="e.g. Follow-up" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Test Done</label>
              <input v-model="form.test_done" class="form-control" placeholder="e.g. ECG" />
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Diagnosis</label>
              <input v-model="form.diagnosis" class="form-control" placeholder="Diagnosis" />
            </div>
            <div class="col-md-6">
              <label class="form-label">Prescription</label>
              <input v-model="form.prescription" class="form-control" placeholder="Prescription" />
            </div>
          </div>

          <div class="mb-3">
            <h5>Medicines</h5>
            <div v-for="(m, idx) in form.medicines" :key="idx" class="d-flex gap-2 mb-2 align-items-center">
              <input v-model="m.name" class="form-control" placeholder="Medicine name" />
              <input v-model="m.dosage" class="form-control" placeholder="dosage (e.g. 1-0-1)" />
              <button type="button" class="btn btn-danger btn-sm" @click="removeMedicine(idx)">Remove</button>
            </div>
            <button type="button" class="btn btn-secondary btn-sm" @click="addMedicine">Add Medicine</button>
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button type="submit" class="btn btn-success" :disabled="saving">Save</button>
            <button type="button" class="btn btn-secondary" @click="$emit('cancel')">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UpdatePatientHistroy',
  props: {
    patientId: { type: Number, required: true },
    patientName: { type: String, default: '' },
    department: { type: String, default: '' }
  },
  data() {
    return {
      form: {
        visit_type: '',
        test_done: '',
        diagnosis: '',
        prescription: '',
        medicines: [ { name: '', dosage: '' } ]
      },
      saving: false
    }
  },
  methods: {
    addMedicine() {
      this.form.medicines.push({ name: '', dosage: '' })
    },
    removeMedicine(idx) {
      this.form.medicines.splice(idx, 1)
      if (this.form.medicines.length === 0) this.addMedicine()
    },
    async saveHistory() {
      this.saving = true
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(`/api/patient/${this.patientId}/history`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
          },
          body: JSON.stringify(this.form)
        })

        if (!res.ok) {
          const err = await res.json().catch(()=>({msg:'failed'}))
          alert('Save failed: ' + (err.msg || res.statusText))
          return
        }

        const data = await res.json().catch(()=>({}))
        this.$emit('saved', data)
      } catch (e) {
        alert('Failed to save history')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
