<template>
  <div class="appointment-container">
    <div class="header-section">
      <div class="header-content">
        <div>
          <h1 class="page-title">Book an Appointment</h1>
          <p class="header-subtitle">Schedule a consultation with your preferred doctor</p>
        </div>
        <div class="nav-links">
          <router-link to="/user_dashboard" class="nav-link">
            <i class="fas fa-home"></i> Dashboard
          </router-link>
          <router-link to="/history" class="nav-link">
            <i class="fas fa-history"></i> History
          </router-link>
          <button @click="logout" class="nav-link logout-btn">
            <i class="fas fa-sign-out-alt"></i> Logout
          </button>
        </div>
      </div>
    </div>

    <div class="doctor-info-card" v-if="doctorInfo">
      <div class="doctor-avatar">
        <i class="fas fa-user-md"></i>
      </div>
      <div class="doctor-details">
        <h2 class="doctor-name">{{ doctorInfo.name }}</h2>
        <p class="specialization">
          <span class="badge-primary">{{ doctorInfo.specialization }}</span>
        </p>
        <div class="doctor-meta">
          <div class="meta-item">
            <i class="fas fa-certificate"></i>
            <span><strong>Qualification:</strong> {{ doctorInfo.qualification }}</span>
          </div>
          <div class="meta-item">
            <i class="fas fa-clock"></i>
            <span><strong>Experience:</strong> {{ doctorInfo.experience }} years</span>
          </div>
        </div>
      </div>
    </div>

    <button @click="goBack" class="back-btn">
      <i class="fas fa-chevron-left"></i> Back
    </button>

    <div class="slots-section">
      <div class="slots-header">
        <h3 class="slots-title">
          <i class="fas fa-calendar-alt"></i> Next 7 Days Availability
        </h3>
        <p class="slots-subtitle">Select a date and time that works best for you</p>
      </div>
      
      <div v-if="!currentUser || !currentUser.id" class="alert-profile">
        <i class="fas fa-exclamation-circle"></i>
        <div>
          <p class="alert-title">Complete Your Profile</p>
          <p class="alert-text">Please complete your profile first to book an appointment.</p>
          <router-link to="/edit-profile" class="btn-profile">Complete Profile</router-link>
        </div>
      </div>
      <div v-else-if="loadingSlots" class="loading-container">
        <div class="spinner"></div>
        <p>Loading available slots...</p>
      </div>
      <div v-else-if="appointmentSlots.length === 0" class="no-slots">
        <i class="fas fa-calendar-times"></i>
        <p>No appointment slots available</p>
      </div>
      <div v-else class="slots-grid">
        <div v-for="day in slotsByDate" :key="day.date" class="day-group">
          <div class="day-group-header">
            <div>
              <span class="day-group-title">{{ day.dayOfWeek }}, {{ day.month }} {{ day.dateNumber }}</span>
              <span class="day-group-meta">{{ day.availableCount }} available / {{ day.totalSlots }} slots</span>
            </div>
            <span v-if="day.allBooked" class="day-all-booked">All slots booked</span>
          </div>

          <div class="day-slot-grid">
            <div
              v-for="slot in day.slots"
              :key="slot.id"
              :class="['slot-card', getSlotCardClass(slot)]"
            >
              <div class="slot-header" :class="{ 'unavailable': !slot.available }">
                <div class="slot-date">
                  <div class="date-day">{{ slot.dateNumber }}</div>
                  <div class="date-month">{{ slot.month }}</div>
                </div>
                <div class="slot-day">{{ slot.dayOfWeek }}</div>
              </div>

              <div class="slot-body">
                <div class="time-display">
                  <i class="fas fa-clock"></i>
                  {{ slot.startTime }} - {{ slot.endTime }}
                </div>
                <div class="slot-status">
                  <span v-if="slot.status === 'Booked'" class="status-badge booked-badge">
                    <i class="fas fa-check-circle"></i> Booked
                  </span>
                  <span v-else-if="!slot.available" class="status-badge unavailable-badge">
                    <i class="fas fa-ban"></i> Not Available
                  </span>
                  <span v-else class="status-badge available-badge">
                    <i class="fas fa-plus-circle"></i> Available
                  </span>
                </div>

                <button
                  v-if="slot.available && slot.status !== 'Booked'"
                  @click="bookAppointment(slot)"
                  class="action-btn book-btn"
                  :disabled="bookingLoading === slot.id"
                >
                  <i class="fas fa-calendar-check"></i>
                  {{ bookingLoading === slot.id ? 'Booking...' : 'Book Now' }}
                </button>
                <button
                  v-else-if="slot.status === 'Booked' && slot.bookedByMe"
                  @click="cancelAppointment(slot)"
                  class="action-btn cancel-btn"
                  :disabled="cancellingLoading === slot.id"
                >
                  <i class="fas fa-trash-alt"></i>
                  {{ cancellingLoading === slot.id ? 'Cancelling...' : 'Cancel' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="successMessage" class="notification success-notification">
      <div class="notification-content">
        <i class="fas fa-check-circle"></i>
        <div>
          <p class="notification-title">Success</p>
          <p class="notification-message">{{ successMessage }}</p>
        </div>
      </div>
      <button class="notification-close" @click="successMessage = ''">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div v-if="errorMessage" class="notification error-notification">
      <div class="notification-content">
        <i class="fas fa-exclamation-circle"></i>
        <div>
          <p class="notification-title">Error</p>
          <p class="notification-message">{{ errorMessage }}</p>
        </div>
      </div>
      <button class="notification-close" @click="errorMessage = ''">
        <i class="fas fa-times"></i>
      </button>
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
  computed: {
    slotsByDate() {
      const grouped = {}

      this.appointmentSlots.forEach(slot => {
        if (!grouped[slot.date]) {
          grouped[slot.date] = {
            date: slot.date,
            dayOfWeek: slot.dayOfWeek,
            dateNumber: slot.dateNumber,
            month: slot.month,
            slots: []
          }
        }

        grouped[slot.date].slots.push(slot)
      })

      return Object.values(grouped)
        .map(group => {
          const availableCount = group.slots.filter(s => s.available && s.status !== 'Booked').length
          const totalSlots = group.slots.length
          const allBooked = group.slots.every(s => s.status === 'Booked' || !s.available)
          return {
            ...group,
            availableCount,
            totalSlots,
            allBooked
          }
        })
        .sort((a, b) => new Date(a.date) - new Date(b.date))
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

        // Full day slot from 9:00 AM to 5:00 PM
        const startTime = '09:00'
        const endTime = '17:00'

        slots.push({
          id: `slot-${this.doctorId}-${currentDate.toISOString().split('T')[0]}`,
          doctorId: this.doctorId,
          date: currentDate.toISOString().split('T')[0],
          dateNumber: dateNumber,
          month: month,
          dayOfWeek: dayOfWeek,
          startTime: startTime,
          endTime: endTime,
          available: isAvailable,
          status: 'Open',
          bookedByMe: false,
          appointmentId: null
        })
      }

      this.appointmentSlots = slots
    },

    checkDoctorAvailability(date) {
      // Hospital operates all 7 days, so every date is available by default
      return true
    },

    getSlotCardClass(slot) {
      if (!slot.available) {
        return 'unavailable'
      } else if (slot.status === 'Booked') {
        return 'booked'
      } else {
        return 'available'
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

        // Parse the start time from the slot
        const [hours, minutes] = slot.startTime.split(':')
        const appointmentDate = new Date(slot.date)
        appointmentDate.setHours(parseInt(hours), parseInt(minutes), 0, 0)

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
        slot.available = false
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

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.appointment-container {
  background: #f2e8d8;
  min-height: 100vh;
  padding: 2rem 1rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    sans-serif;
}

/* Animations */
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes cardSlide {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Header Styles */
.header-section {
  background: #fffdf7;
  border-radius: 24px;
  border: 1px solid #d8c8b0;
  padding: 2rem 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  color: #3d362f;
  animation: slideDown 0.5s ease-out;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.header-subtitle {
  font-size: 1rem;
  color: #6d5f53;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #3d362f;
  text-decoration: none;
  font-weight: 700;
  padding: 0.6rem 1rem;
  border-radius: 999px;
  background: #f4e9db;
  border: 1px solid #d8c8b0;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.nav-link:hover {
  background: #e8dcc9;
  border-color: #8f7b65;
  transform: translateY(-2px);
}

.logout-btn {
  background: rgba(138, 90, 90, 0.1);
  border-color: #8a5a5a;
  color: #3d362f;
}

.logout-btn:hover {
  background: rgba(138, 90, 90, 0.15);
  border-color: #8f7b65;
}

/* Doctor Info Card */
.doctor-info-card {
  background: #fffdf7;
  border-radius: 24px;
  border: 1px solid #d8c8b0;
  padding: 1.5rem;
  margin-bottom: 2rem;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.05);
  border-top: 4px solid #8f7b65;
  max-width: 1400px;
  transition: all 0.3s ease;
  animation: cardSlide 0.5s ease-out;
}

.doctor-info-card:hover {
  box-shadow: 0 22px 50px rgba(0, 0, 0, 0.08);
  transform: translateY(-3px);
}

.doctor-avatar {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: #8f7b65;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 2.5rem;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.25);
}

.doctor-details {
  flex: 1;
}

.doctor-name {
  font-size: 1.5rem;
  font-weight: 800;
  color: #3d362f;
  margin-bottom: 0.75rem;
}

.specialization {
  margin-bottom: 1rem;
}

.badge-primary {
  background: #8f7b65;
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 999px;
  font-size: 0.9rem;
  font-weight: 700;
  display: inline-block;
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.25);
}

.doctor-meta {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #7d6d5f;
  font-size: 0.95rem;
}

.meta-item i {
  color: #8f7b65;
  font-size: 1rem;
}

/* Back Button */
.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: #fffdf7;
  border: 1px solid #d8c8b0;
  border-radius: 999px;
  color: #8f7b65;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 2rem;
  margin-left: auto;
  margin-right: auto;
  width: fit-content;
  font-size: 0.95rem;
}

.back-btn:hover {
  border-color: #8f7b65;
  color: #3d362f;
  background: #f4e9db;
  transform: translateY(-2px);
}

/* Slots Section */
.slots-section {
  max-width: 1400px;
  margin: 0 auto;
}

.slots-header {
  margin-bottom: 2rem;
}

.slots-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #3d362f;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.slots-title i {
  color: #8f7b65;
}

.slots-subtitle {
  color: #7d6d5f;
  font-size: 0.95rem;
  margin: 0;
}

/* Alert Styles */
.alert-profile {
  background: #fff7f0;
  border: 1px solid #d7c7b5;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(143, 123, 101, 0.1);
  animation: slideUp 0.5s ease-out;
}

.alert-profile i {
  color: #8f7b65;
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.alert-title {
  font-weight: 800;
  color: #3d362f;
  margin-bottom: 0.25rem;
}

.alert-text {
  color: #7d6d5f;
  margin: 0 0 1rem 0;
}

.btn-profile {
  display: inline-flex;
  align-items: center;
  padding: 0.6rem 1.5rem;
  background: #8f7b65;
  color: white;
  text-decoration: none;
  border-radius: 999px;
  font-weight: 700;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-profile:hover {
  background: #7a6a58;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(143, 123, 101, 0.3);
}

/* Loading Spinner */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 2rem;
  text-align: center;
  color: #7d6d5f;
  background: #fffdf7;
  border-radius: 16px;
  border: 1px solid #d8c8b0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e3d3c1;
  border-top-color: #8f7b65;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* No Slots Message */
.no-slots {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 3rem 2rem;
  color: #6d5f53;
  text-align: center;
  background: #fffdf7;
  border-radius: 16px;
  border: 1px solid #d8c8b0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.no-slots i {
  font-size: 3rem;
  color: #ddd;
}

/* Slots Grid */
.slots-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  animation: slideUp 0.5s ease-out;
}

.day-group {
  background: #fffdf7;
  border: 1px solid #d8c8b0;
  border-radius: 18px;
  padding: 1rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
}

.day-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.day-group-title {
  font-weight: 800;
  color: #3d362f;
}

.day-group-meta {
  color: #7d6d5f;
  font-size: 0.9rem;
}

.day-all-booked {
  background: #f8d7da;
  color: #842029;
  border-radius: 999px;
  padding: 0.4rem 0.9rem;
  font-size: 0.75rem;
  font-weight: 700;
}

.day-slot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

/* Slot Card */
.slot-card {
  background: #fffdf7;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #d8c8b0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  animation: cardSlide 0.5s ease-out;
}

.slot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}

.slot-card.available {
  border-color: #8f7b65;
  border-top: 4px solid #8f7b65;
}

.slot-card.available:hover {
  border-color: #8f7b65;
}

.slot-card.booked {
  border-color: #d7c7b5;
  border-top: 4px solid #d7c7b5;
}

.slot-card.unavailable {
  border-color: #ddd;
  opacity: 0.6;
}

/* Slot Header */
.slot-header {
  background: #f4e9db;
  color: #3d362f;
  padding: 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(143, 123, 101, 0.1);
  border-bottom: 1px solid #dacbb8;
}

.slot-header.unavailable {
  background: #efefef;
  color: #999;
}

.slot-date {
  text-align: left;
}

.date-day {
  font-size: 1.2rem;
  font-weight: 800;
  line-height: 1;
  margin-bottom: 0.15rem;
  color: #8f7b65;
}

.date-month {
  font-size: 0.75rem;
  font-weight: 700;
  color: #7d6d5f;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.slot-day {
  font-size: 0.75rem;
  font-weight: 700;
  text-align: right;
  color: #3d362f;
}

/* Slot Body */
.slot-body {
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  flex: 1;
}

.time-display {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  color: #7d6d5f;
  font-size: 0.8rem;
  font-weight: 600;
}

.time-display i {
  color: #8f7b65;
  font-size: 0.75rem;
}

/* Status Badges */
.slot-status {
  display: flex;
  justify-content: center;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.8rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.available-badge {
  background: rgba(85, 158, 104, 0.15);
  color: #3d5f3d;
  border: 1px solid #559e68;
}

.booked-badge {
  background: rgba(215, 199, 181, 0.3);
  color: #6d5f53;
  border: 1px solid #d7c7b5;
}

.unavailable-badge {
  background: rgba(138, 90, 90, 0.15);
  color: #5c3d3d;
  border: 1px solid #8a5a5a;
}

/* Action Buttons */
.action-btn {
  padding: 0.5rem 0.8rem;
  border: 1px solid #d8c8b0;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.7rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  width: 100%;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: #f4e9db;
  color: #3d362f;
  white-space: nowrap;
}

.action-btn:hover {
  transform: translateY(-2px);
}

.book-btn {
  color: #8f7b65;
  border-color: #8f7b65;
  background: #f0e5d8;
}

.book-btn:hover:not(:disabled) {
  background: #e8dcc9;
  border-color: #8f7b65;
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.2);
}

.book-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-btn {
  color: #8a5a5a;
  border-color: #8a5a5a;
  background: rgba(138, 90, 90, 0.08);
}

.cancel-btn:hover:not(:disabled) {
  background: rgba(138, 90, 90, 0.15);
  border-color: #8a5a5a;
  box-shadow: 0 4px 12px rgba(138, 90, 90, 0.2);
}

.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Notifications */
.notification {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  max-width: 420px;
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  animation: slideIn 0.3s ease;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.success-notification {
  background: #f0f9f0;
  border: 1px solid #b8dab8;
}

.error-notification {
  background: #fef5f5;
  border: 1px solid #dbb8b8;
}

.notification-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  flex: 1;
}

.notification-content i {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.success-notification i {
  color: #559e68;
}

.error-notification i {
  color: #a65c5c;
}

.notification-title {
  font-weight: 800;
  margin-bottom: 0.25rem;
}

.success-notification .notification-title {
  color: #3d5f3d;
}

.error-notification .notification-title {
  color: #5c3d3d;
}

.notification-message {
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.85;
}

.success-notification .notification-message {
  color: #3d5f3d;
}

.error-notification .notification-message {
  color: #5c3d3d;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.success-notification .notification-close {
  color: #559e68;
}

.error-notification .notification-close {
  color: #a65c5c;
}

.notification-close:hover {
  transform: scale(1.2);
}

/* Responsive Design */
@media (max-width: 768px) {
  .appointment-container {
    padding: 1rem;
  }

  .header-section {
    padding: 1.5rem 1rem;
    margin-bottom: 1.5rem;
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .header-subtitle {
    font-size: 0.9rem;
  }

  .nav-links {
    width: 100%;
    gap: 0.75rem;
  }

  .nav-link {
    flex: 1;
    justify-content: center;
    font-size: 0.85rem;
    padding: 0.5rem 0.75rem;
  }

  .doctor-info-card {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }

  .doctor-avatar {
    margin: 0 auto;
  }

  .doctor-meta {
    justify-content: center;
    flex-direction: column;
  }

  .meta-item {
    justify-content: center;
  }

  .back-btn {
    display: flex;
    justify-content: center;
  }

  .slots-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1rem;
  }

  .slot-card {
    border-radius: 10px;
  }

  .slot-header {
    padding: 1rem;
  }

  .date-day {
    font-size: 1.5rem;
  }

  .slot-body {
    padding: 1rem;
    gap: 0.75rem;
  }

  .notification {
    right: 1rem;
    left: 1rem;
    max-width: none;
  }

  .slots-title {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .appointment-container {
    padding: 0.75rem;
  }

  .header-section {
    padding: 1rem;
    border-radius: 10px;
  }

  .page-title {
    font-size: 1.3rem;
  }

  .header-subtitle {
    font-size: 0.8rem;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    gap: 0.25rem;
  }

  .doctor-info-card {
    padding: 1rem;
    gap: 1rem;
  }

  .doctor-name {
    font-size: 1.2rem;
  }

  .doctor-avatar {
    width: 60px;
    height: 60px;
    font-size: 2rem;
  }

  .slots-grid {
    grid-template-columns: 1fr;
  }

  .slot-header {
    padding: 1rem;
  }

  .date-day {
    font-size: 1.4rem;
  }

  .action-btn {
    font-size: 0.75rem;
    padding: 0.5rem 0.75rem;
  }

  .notification {
    top: 1rem;
    right: 0.5rem;
    left: 0.5rem;
    font-size: 0.85rem;
  }
}
</style>


