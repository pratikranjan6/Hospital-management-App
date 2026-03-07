<template>
  <div class="container-fluid py-4">
    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <h1 class="h3 mb-0">Book Appointment</h1>
          <div class="d-flex align-items-center gap-3">
            <router-link to="/user_dashboard" class="text-decoration-none">Dashboard</router-link>
            <span class="text-muted">|</span>
            <router-link to="/history" class="text-decoration-none">History</router-link>
            <span class="text-muted">|</span>
            <button @click="logout" class="btn btn-link p-0 text-decoration-none">logout</button>
          </div>
        </div>
      </div>
    </div>

    <div class="card mb-4" v-if="doctorInfo">
      <div class="card-body">
        <h2 class="h4 mb-3">{{ doctorInfo.name }}</h2>
        <p><strong>Specialization:</strong> {{ doctorInfo.specialization }}</p>
        <p><strong>Qualification:</strong> {{ doctorInfo.qualification }}</p>
        <p><strong>Experience:</strong> {{ doctorInfo.experience }} years</p>
      </div>
    </div>

    <button @click="goBack" class="btn btn-secondary mb-4">← Back</button>

    <div class="card">
      <div class="card-body">
        <h3 class="h5 mb-4">Next 7 Days Availability</h3>
        
        <div v-if="!currentUser || !currentUser.id" class="alert alert-warning" role="alert">
          <p class="mb-2">Please complete your profile first to book an appointment.</p>
          <router-link to="/edit-profile" class="btn btn-warning btn-sm">Complete Profile</router-link>
        </div>
        <div v-else-if="loadingSlots" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading appointment slots...</span>
          </div>
        </div>
        <div v-else-if="appointmentSlots.length === 0" class="text-center py-4 text-muted">
          No appointment slots available
        </div>
        <div v-else class="row g-3">
          <div
            v-for="slot in appointmentSlots"
            :key="slot.id"
            class="col-12 col-sm-6 col-md-4 col-lg-3"
          >
            <div 
              class="card h-100 text-center"
              :class="getSlotCardClass(slot)"
            >
              <div class="card-body d-flex flex-column justify-content-between">
                <div class="slot-date mb-3">
                  <div class="fs-4 fw-bold text-primary">{{ slot.dateNumber }}</div>
                  <div class="small text-muted text-uppercase">{{ slot.month }}</div>
                  <div class="fw-semibold">{{ slot.dayOfWeek }}</div>
                </div>

                <div>
                  <div v-if="slot.available" class="small text-muted mb-2">
                    {{ slot.startTime }} - {{ slot.endTime }}
                  </div>
                  <div class="mb-3">
                    <span v-if="!slot.available" class="badge bg-danger">
                      No Appointment
                    </span>
                    <span v-else-if="slot.status === 'Booked'" class="badge bg-warning">
                      Booked
                    </span>
                    <span v-else class="badge bg-success">
                      Available
                    </span>
                  </div>

                  <button
                    v-if="slot.available && slot.status !== 'Booked'"
                    @click="bookAppointment(slot)"
                    class="btn btn-success btn-sm w-100"
                    :disabled="bookingLoading === slot.id"
                  >
                    {{ bookingLoading === slot.id ? 'Booking...' : 'Book' }}
                  </button>
                  <button
                    v-else-if="slot.status === 'Booked' && slot.bookedByMe"
                    @click="cancelAppointment(slot)"
                    class="btn btn-danger btn-sm w-100"
                    :disabled="cancellingLoading === slot.id"
                  >
                    {{ cancellingLoading === slot.id ? 'Cancelling...' : 'Cancel' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="successMessage" class="alert alert-success alert-dismissible fade show position-fixed top-0 end-0 m-3" role="alert" style="z-index: 1000; width: auto; max-width: 400px;">
      {{ successMessage }}
      <button type="button" class="btn-close" @click="successMessage = ''" aria-label="Close"></button>
    </div>

    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show position-fixed top-0 end-0 m-3" role="alert" style="z-index: 1000; width: auto; max-width: 400px;">
      {{ errorMessage }}
      <button type="button" class="btn-close" @click="errorMessage = ''" aria-label="Close"></button>
    </div>
  </div>
</template>

<script>
import { getApiBase, getAuthHeader } from '../utils/auth'

export default {
  name: 'BookAppointment',
  data() {
    return {
      doctorId: null,
      doctorInfo: null,
      appointmentSlots: [],
      loadingSlots: true,
      bookingLoading: null,
      cancellingLoading: null,
      successMessage: '',
      errorMessage: '',
      currentUser: null
    }
  },
  mounted() {
    this.initializeComponent()
  },
  methods: {
    async initializeComponent() {
      try {
     
        this.doctorId = this.$route.params.doctorId || this.$route.query.doctorId
        
        if (!this.doctorId) {
          this.errorMessage = 'Doctor ID not found'
          setTimeout(() => {
            this.$router.push('/user_dashboard')
          }, 2000)
          return
        }

     
        await this.fetchCurrentUserInfo()
        
    
        await this.fetchDoctorInfo()
        
        
        if (this.currentUser && this.currentUser.id) {
          await this.fetch7DaySlots()
        } else {
          this.loadingSlots = false
        }
      } catch (error) {
        console.error('Error initializing component:', error)
        this.errorMessage = 'Failed to load appointment booking page'
      }
    },

    async fetchCurrentUserInfo() {
      try {
        const response = await fetch(`${getApiBase()}/api/patient/profile`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (response.ok) {
          const data = await response.json()
          this.currentUser = {
            patient_id: data.id,
            ...data
          }
        }
      } catch (error) {
        console.error('Error fetching current user:', error)
      }
    },

    async fetchDoctorInfo() {
      try {
        const response = await fetch(
          `${getApiBase()}/api/doctors/${this.doctorId}`,
          {
            method: 'GET',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          throw new Error('Failed to fetch doctor info')
        }

        const doctors = await response.json()
        if (Array.isArray(doctors) && doctors.length > 0) {
          this.doctorInfo = doctors[0]
        }
      } catch (error) {
        console.error('Error fetching doctor info:', error)
      }
    },

    async fetch7DaySlots() {
      try {
        this.loadingSlots = true

        const response = await fetch(
          `${getApiBase()}/api/doctor/${this.doctorId}/7day-slots`,
          {
            method: 'GET',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
         
          this.generateLocal7DaySlots()
          return
        }

        const data = await response.json()
        this.appointmentSlots = data
      } catch (error) {
        console.error('Error fetching 7-day slots:', error)
      
        this.generateLocal7DaySlots()
      } finally {
        this.loadingSlots = false
      }
    },

    generateLocal7DaySlots() {
      const slots = []
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      for (let i = 0; i < 7; i++) {
        const currentDate = new Date(today)
        currentDate.setDate(today.getDate() + i)

        const dayOfWeek = currentDate.toLocaleDateString('en-US', {
          weekday: 'short'
        })
        const dateNumber = currentDate.getDate()
        const month = currentDate.toLocaleDateString('en-US', {
          month: 'short'
        })

  
        const isAvailable = this.checkDoctorAvailability(currentDate)

        slots.push({
          id: `slot-${i}`,
          doctorId: this.doctorId,
          date: currentDate.toISOString().split('T')[0],
          dateNumber: dateNumber,
          month: month,
          dayOfWeek: dayOfWeek,
          startTime: '09:00',
          endTime: '17:00',
          available: isAvailable,
          status: 'Open',
          bookedByMe: false,
          appointmentId: null
        })
      }

      this.appointmentSlots = slots
    },

    checkDoctorAvailability(date) {
     
      const dayOfWeek = date.getDay()
      if (dayOfWeek === 0 || dayOfWeek === 6) {
        return false
      }
      return true
    },

    getSlotCardClass(slot) {
      if (!slot.available) {
        return 'border-danger'
      } else if (slot.status === 'Booked') {
        return 'border-warning'
      } else {
        return 'border-success'
      }
    },

    async bookAppointment(slot) {
      try {
        if (!this.currentUser || !this.currentUser.id) {
          this.errorMessage = 'Please complete your profile first. Redirecting to profile page...'
          setTimeout(() => {
            this.$router.push('/edit-profile')
          }, 2000)
          return
        }

        this.bookingLoading = slot.id

     
        const appointmentDate = new Date(slot.date)
        appointmentDate.setHours(9, 0, 0, 0) 

        const appointmentData = {
          patient_id: this.currentUser.id,
          doctor_id: this.doctorId,
          department_id: this.doctorInfo.specialization_id || 1,
          appointment_date: appointmentDate.toISOString(),
          status: 'Booked'
        }

        const response = await fetch(`${getApiBase()}/api/appointment/book`, {
          method: 'POST',
          headers: {
            ...getAuthHeader(),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(appointmentData)
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.msg || 'Failed to book appointment')
        }

        const result = await response.json()

  
        slot.status = 'Booked'
        slot.bookedByMe = true
        slot.appointmentId = result.appointment_id

        this.successMessage = 'Appointment booked successfully!'
        setTimeout(() => {
          this.successMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error booking appointment:', error)
        this.errorMessage = error.message || 'Failed to book appointment'
      } finally {
        this.bookingLoading = null
      }
    },

    async cancelAppointment(slot) {
      try {
        if (!slot.appointmentId) {
          this.errorMessage = 'Appointment ID not found'
          return
        }

        this.cancellingLoading = slot.id

        const response = await fetch(
          `${getApiBase()}/api/user/appointment/${slot.appointmentId}`,
          {
            method: 'DELETE',
            headers: getAuthHeader()
          }
        )

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.msg || 'Failed to cancel appointment')
        }


        slot.status = 'Open'
        slot.bookedByMe = false
        slot.appointmentId = null

        this.successMessage = 'Appointment cancelled successfully'
        setTimeout(() => {
          this.successMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error cancelling appointment:', error)
        this.errorMessage = error.message || 'Failed to cancel appointment'
      } finally {
        this.cancellingLoading = null
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


