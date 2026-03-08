<template>
  <div class="container-fluid py-4">
    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <h1 class="h3 mb-0">{{ department.name }}</h1>
          <div class="d-flex align-items-center gap-3">
            <router-link to="/history" class="text-decoration-none">History</router-link>
            <span class="text-muted">|</span>
            <button @click="logout" class="btn btn-link p-0 text-decoration-none">logout</button>
          </div>
        </div>
      </div>
    </div>

    <button @click="goBack" class="btn btn-secondary mb-4">← Back to Dashboard</button>

    <div class="card mb-4">
      <div class="card-body">
        <h2 class="h4 mb-3">Overview</h2>
        <p class="text-justify">{{ department.description }}</p>
      </div>
    </div>

    <div class="card">
      <div class="card-body">
        <h2 class="h4 mb-3">Doctors' list</h2>
        <form class="d-flex mb-3" @submit.prevent="searchDoctors">
          <input
            v-model="searchQuery"
            class="form-control me-2"
            type="search"
            placeholder="Search doctors by name"
            aria-label="Search doctors"
          />
          <button class="btn btn-outline-primary" type="submit">Search</button>
        </form>
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading doctors...</span>
          </div>
        </div>
        <div v-else-if="doctors.length === 0" class="text-center py-4 text-muted">No doctors available in this department</div>
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <tbody>
              <tr v-for="doctor in doctors" :key="doctor.id">
                <td class="fw-semibold">{{ doctor.name }}</td>
                <td class="text-end">
                  <button @click="checkAvailability(doctor)" class="btn btn-outline-primary btn-sm me-2">
                    check availability
                  </button>
                  <button @click="viewDoctorDetails(doctor)" class="btn btn-outline-secondary btn-sm">
                    view details
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="showDoctorModal" class="modal fade show d-block" tabindex="-1" @click.self="closeDoctorModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedDoctor.name }}</h5>
            <button type="button" class="btn-close" @click="closeDoctorModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>Specialization:</strong> {{ selectedDoctor.specialization }}</p>
            <p><strong>Qualification:</strong> {{ selectedDoctor.qualification }}</p>
            <p><strong>Experience:</strong> {{ selectedDoctor.experience }} years</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="closeDoctorModal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showDoctorModal" class="modal-backdrop fade show"></div>

    <div v-if="showAvailabilityModal" class="modal fade show d-block" tabindex="-1" @click.self="closeAvailabilityModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedDoctor.name }} - Availability</h5>
            <button type="button" class="btn-close" @click="closeAvailabilityModal"></button>
          </div>
          <div class="modal-body">
            <p v-if="doctorAvailability.length === 0" class="text-muted">No availability information available</p>
            <div v-else class="d-flex flex-column gap-3">
              <div v-for="availability in doctorAvailability" :key="availability.id" class="border p-3 rounded bg-light">
                <p class="mb-1"><strong>Date:</strong> {{ formatDate(availability.date) }}</p>
                <p class="mb-1"><strong>Status:</strong> <span class="badge" :class="getStatusBadgeClass(availability.status)">{{ availability.status }}</span></p>
                <p v-if="availability.start_time" class="mb-0"><strong>Time:</strong> {{ availability.start_time }} - {{ availability.end_time }}</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="closeAvailabilityModal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showAvailabilityModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'DepartmentInfo',
  data() {
    return {
      department: {},
      doctors: [],
      searchQuery: '',
      loading: true,
      showDoctorModal: false,
      showAvailabilityModal: false,
      selectedDoctor: {},
      doctorAvailability: []
    }
  },
  methods: {
    async fetchDepartmentData() {
      try {
        const departmentId = this.$route.params.id
        if (!departmentId) {
          const sessionDept = this.$route.query.department
          if (sessionDept) {
            this.department = JSON.parse(decodeURIComponent(sessionDept))
          } else {
            this.$router.push('/user_dashboard')
            return
          }
        }
      } catch (error) {
        console.error('Error parsing department:', error)
        this.$router.push('/user_dashboard')
      }
    },

    async fetchDoctors() {
      try {
        this.loading = true
        const departmentId = this.department.id

        const response = await fetch(
          `${getApiBase()}/api/department/${departmentId}/doctors`,
          {
            method: 'GET',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          throw new Error('Failed to fetch doctors')
        }

        this.doctors = await response.json()
      } catch (error) {
        console.error('Error fetching doctors:', error)
        this.$toast?.error?.('Failed to fetch doctors')
      } finally {
        this.loading = false
      }
    },

    async searchDoctors() {
      try {
        this.loading = true
        const departmentId = this.department.id
        let url = `${getApiBase()}/api/department/${departmentId}/doctors`
        if (this.searchQuery.trim()) {
          url += `?q=${encodeURIComponent(this.searchQuery.trim())}`
        }

        const response = await fetch(url, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to search doctors')
        }

        this.doctors = await response.json()
      } catch (error) {
        console.error('Error searching doctors:', error)
        this.$toast?.error?.('Failed to search doctors')
      } finally {
        this.loading = false
      }
    },

    async fetchDoctorAvailability(doctorId) {
      try {
        const response = await fetch(
          `${getApiBase()}/api/doctor/${doctorId}/availability`,
          {
            method: 'GET',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          this.doctorAvailability = []
          return
        }

        this.doctorAvailability = await response.json()
      } catch (error) {
        console.error('Error fetching availability:', error)
        this.doctorAvailability = []
      }
    },

    viewDoctorDetails(doctor) {
      this.selectedDoctor = doctor
      this.showDoctorModal = true
    },

    closeDoctorModal() {
      this.showDoctorModal = false
      this.selectedDoctor = {}
    },

    async checkAvailability(doctor) {
      this.$router.push({
        name: 'bookAppointment',
        params: { doctorId: doctor.id },
        query: { doctorName: doctor.name }
      })
    },

    closeAvailabilityModal() {
      this.showAvailabilityModal = false
      this.selectedDoctor = {}
      this.doctorAvailability = []
    },

    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-GB')
    },

    getStatusBadgeClass(status) {
      const lowerStatus = status.toLowerCase()
      if (lowerStatus === 'available') return 'bg-success'
      if (lowerStatus === 'unavailable' || lowerStatus === 'not available') return 'bg-danger'
      return 'bg-info'
    },

    goBack() {
      this.$router.back()
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      this.$router.push('/login')
    }
  },

  mounted() {
    const passedDept = this.$route.params.department
    if (passedDept) {
      try {
        this.department = typeof passedDept === 'string' ? JSON.parse(passedDept) : passedDept
      } catch (error) {
        this.department = passedDept
      }
    }

    if (this.$route.query.department) {
      try {
        this.department = JSON.parse(decodeURIComponent(this.$route.query.department))
      } catch (error) {
      }
    }

    if (this.department && this.department.id) {
      this.fetchDoctors()
    } else {
      this.$router.push('/user_dashboard')
    }
  }
}
</script>


