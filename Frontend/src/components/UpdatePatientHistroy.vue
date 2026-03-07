<template>
  <div class="update-history">
    <h2>Update Patient History</h2>

    <div class="patient-info">
      <div><strong>Patient Name:</strong> {{ patientName }}</div>
      <div><strong>Department:</strong> {{ department || 'N/A' }}</div>
    </div>

    <form @submit.prevent="saveHistory" class="history-form">
      <div class="row">
        <label>Visit Type</label>
        <input v-model="form.visit_type" placeholder="e.g. Follow-up" />

        <label>Test Done</label>
        <input v-model="form.test_done" placeholder="e.g. ECG" />
      </div>

      <div class="row">
        <label>Diagnosis</label>
        <input v-model="form.diagnosis" placeholder="Diagnosis" />

        <label>Prescription</label>
        <input v-model="form.prescription" placeholder="Prescription" />
      </div>

      <div class="medicines">
        <div class="med-header">Medicines</div>
        <div v-for="(m, idx) in form.medicines" :key="idx" class="medicine-row">
          <input v-model="m.name" placeholder="Medicine name" />
          <input v-model="m.dosage" placeholder="dosage (e.g. 1-0-1)" />
          <button type="button" class="btn small danger" @click="removeMedicine(idx)">remove</button>
        </div>
        <button type="button" class="btn small" @click="addMedicine">add medicine</button>
      </div>

      <div class="actions">
        <button type="submit" class="btn save">save</button>
        <button type="button" class="btn cancel" @click="$emit('cancel')">cancel</button>
      </div>
    </form>
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

<style scoped>
.update-history { max-width:980px; border:1px solid #e6eef6; padding:20px; margin: 18px auto; font-family: Inter, Arial, Helvetica, sans-serif; background:#fff; border-radius:8px }
.update-history h2 { margin:0 0 12px 0; text-align:left; color:#0f1724 }
.patient-info { margin-bottom:16px; color:#334155 }
.history-form { display:block }
.row { display:flex; gap:12px; margin-bottom:12px }
.row label { width:120px; font-weight:600; align-self:center; color:#102a43 }
.row input { flex:1; padding:10px; border:1px solid #e2e8f0; border-radius:8px; background:#fbfdff }
.medicines { margin:14px 0 }
.med-header { font-weight:600; margin-bottom:10px; color:#0f1724 }
.medicine-row { display:flex; gap:8px; align-items:center; margin-bottom:8px }
.medicine-row input { padding:8px; border-radius:6px; border:1px solid #e2e8f0 }
.hint { color: #10b981; font-size:13px }
.actions { margin-top:12px; display:flex; gap:8px; justify-content:flex-end }
.btn { padding:8px 12px; border-radius:6px; border:1px solid transparent; cursor:pointer }
.small { padding:6px 8px; font-size:13px }
.danger { background:#ef4444; color:#fff }
.save { background:#10b981; color:#fff }
.cancel { background:#f8fafc }
</style>
