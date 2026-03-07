<template>
  <div class="container-fluid py-4">
    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <h1 class="h3 mb-0">My Medical History</h1>
          <div class="d-flex align-items-center gap-3">
            <router-link to="/user_dashboard" class="text-decoration-none">Dashboard</router-link>
            <span class="text-muted">|</span>
            <button @click="exportHistory" class="btn btn-link p-0 text-decoration-none">Export CSV</button>
            <span class="text-muted">|</span>
            <button @click="logout" class="btn btn-link p-0 text-decoration-none">logout</button>
          </div>
        </div>
      </div>
    </div>

    <button @click="goBack" class="btn btn-secondary mb-4">← Back</button>

    <div class="row">
      <div class="col-12">
        <div class="card mb-4">
          <div class="card-body">
            <h2 class="h5 mb-3">Patient Information</h2>
            <div class="row">
              <div class="col-md-6">
                <div class="mb-3">
                  <strong>Patient Name:</strong> {{ patientName }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <h3 class="h5 mb-4">Visit History</h3>
            
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading history...</span>
              </div>
            </div>
            <div v-else class="table-responsive">
              <table class="table table-striped table-hover">
                <thead class="table-light">
                  <tr>
                    <th>Visit No.</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Date</th>
                    <th>Tests Done</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Medicines</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="visits.length === 0">
                    <td colspan="8" class="text-center text-muted py-4">No visit history found</td>
                  </tr>
                  <tr v-for="(visit, index) in visits" :key="visit.id">
                    <td>{{ index + 1 }}</td>
                    <td>{{ visit.doctor_name || 'N/A' }}</td>
                    <td>{{ visit.department || 'N/A' }}</td>
                    <td>{{ formatDate(visit.date) }}</td>
                    <td>{{ visit.tests_done || 'N/A' }}</td>
                    <td>{{ visit.diagnosis || 'N/A' }}</td>
                    <td>{{ visit.prescription || 'N/A' }}</td>
                    <td>
                      <ul class="list-unstyled mb-0">
                        <li v-if="visit.medicines && visit.medicines.length > 0" v-for="medicine in visit.medicines" :key="medicine" class="mb-1">
                          {{ medicine }}
                        </li>
                        <li v-else class="text-muted">N/A</li>
                      </ul>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="text-end mt-4">
              <button @click="goBack" class="btn btn-secondary">Back</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'UserPatientHistory',
  data() {
    return {
      patientName: 'User',
      visits: [],
      loading: true
    }
  },
  mounted() {
    this.fetchUserHistory()
  },
  methods: {
    async fetchUserHistory() {
      try {
        this.loading = true
        const response = await fetch(`${getApiBase()}/api/patient/history`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to fetch history')
        }

        const data = await response.json()
        this.patientName = data.patient_name || 'User'
        this.visits = Array.isArray(data.appointments) ? data.appointments : []
      } catch (error) {
        console.error('Error fetching patient history:', error)
        this.$toast?.error?.('Failed to load medical history')
      } finally {
        this.loading = false
      }
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-GB')
    },

    async exportHistory() {
      try {
        const response = await fetch(`${getApiBase()}/api/patient/export_history`, {
          method: 'POST',
          headers: getAuthHeader()
        })
        if (!response.ok) {
          throw new Error('Export request failed')
        }
        this.$toast?.success?.('Export started. You will receive an email when it completes.')

        const checkStatus = async () => {
          try {
            const s = await fetch(`${getApiBase()}/api/patient/export_status`, {
              method: 'GET',
              headers: getAuthHeader()
            })
            if (s.ok) {
              const data = await s.json()
              if (data.done) {
                this.$toast?.success?.('Export completed; check your email.')
              } else {
                setTimeout(checkStatus, 5000)
              }
            } else {
              setTimeout(checkStatus, 5000)
            }
          } catch (e) {
            setTimeout(checkStatus, 5000)
          }
        }
        checkStatus()
      } catch (err) {
        console.error('Error starting export:', err)
        this.$toast?.error?.('Failed to start export')
      }
    },

    goBack() {
      this.$router.back()
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.table-hover tbody tr:hover {
  background-color: #f5f5f5;
}

.table th {
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
}

.card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
  font-weight: 500;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

@media (max-width: 768px) {
  .table {
    font-size: 0.9rem;
  }
  
  .table th,
  .table td {
    padding: 0.75rem 0.5rem;
  }
}
</style>
