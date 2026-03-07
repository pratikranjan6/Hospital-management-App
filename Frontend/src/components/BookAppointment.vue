<template>
  <div class="book-appointment">
    <div class="appointment-header">
      <h1>Book Appointment</h1>
      <div class="header-actions">
        <router-link to="/user_dashboard" class="action-link">Dashboard</router-link>
        <span class="divider">|</span>
        <router-link to="/history" class="action-link">History</router-link>
        <span class="divider">|</span>
        <button @click="logout" class="logout-btn">logout</button>
      </div>
    </div>

    <div class="doctor-info-section" v-if="doctorInfo">
      <div class="doctor-card">
        <div class="doctor-details">
          <h2>{{ doctorInfo.name }}</h2>
          <p><strong>Specialization:</strong> {{ doctorInfo.specialization }}</p>
          <p><strong>Qualification:</strong> {{ doctorInfo.qualification }}</p>
          <p><strong>Experience:</strong> {{ doctorInfo.experience }} years</p>
        </div>
      </div>
    </div>

    <button @click="goBack" class="back-btn">← Back</button>

    <div class="slots-section">
      <h3>Next 7 Days Availability</h3>
      
      <div v-if="!currentUser || !currentUser.id" class="warning-message">
        <p>Please complete your profile first to book an appointment.</p>
        <router-link to="/edit-profile" class="profile-link">Complete Profile</router-link>
      </div>
      <div v-else-if="loadingSlots" class="loading">Loading appointment slots...</div>
      <div v-else-if="appointmentSlots.length === 0" class="no-data">
        No appointment slots available
      </div>
      <div v-else class="slots-grid">
        <div
          v-for="slot in appointmentSlots"
          :key="slot.id"
          class="slot-card"
          :class="[
            'day-' + slot.dayOfWeek.toLowerCase(),
            { 'unavailable': !slot.available },
            { 'booked': slot.status === 'Booked' },
            { 'available': slot.available && slot.status !== 'Booked' }
          ]"
        >
          <div class="slot-date">
            <div class="date-number">{{ slot.dateNumber }}</div>
            <div class="date-month">{{ slot.month }}</div>
            <div class="day-name">{{ slot.dayOfWeek }}</div>
          </div>

          <div class="slot-content">
            <div class="slot-time" v-if="slot.available">
              {{ slot.startTime }} - {{ slot.endTime }}
            </div>
            <div class="slot-status">
              <span v-if="!slot.available" class="status-badge unavailable">
                No Appointment
              </span>
              <span v-else-if="slot.status === 'Booked'" class="status-badge booked">
                Booked
              </span>
              <span v-else class="status-badge open">
                Available
              </span>
            </div>

            <button
              v-if="slot.available && slot.status !== 'Booked'"
              @click="bookAppointment(slot)"
              class="book-btn"
              :disabled="bookingLoading === slot.id"
            >
              {{ bookingLoading === slot.id ? 'Booking...' : 'Book Appointment' }}
            </button>
            <button
              v-else-if="slot.status === 'Booked' && slot.bookedByMe"
              @click="cancelAppointment(slot)"
              class="cancel-btn"
              :disabled="cancellingLoading === slot.id"
            >
              {{ cancellingLoading === slot.id ? 'Cancelling...' : 'Cancel Appointment' }}
            </button>
            <div v-else-if="slot.status === 'Booked'" class="booked-by-other">
              Booked by another patient
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
      <button @click="successMessage = ''" class="close-msg">&times;</button>
    </div>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="close-msg">&times;</button>
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

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.book-appointment {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.appointment-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.appointment-header h1 {
  color: #333;
  margin: 0;
  font-size: 28px;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.action-link,
.logout-btn {
  text-decoration: none;
  color: #667eea;
  font-weight: 500;
  border: none;
  background: none;
  cursor: pointer;
  transition: color 0.3s;
  font-size: 14px;
}

.action-link:hover,
.logout-btn:hover {
  color: #764ba2;
}

.divider {
  color: #ccc;
}

/* Doctor Info */
.doctor-info-section {
  margin-bottom: 30px;
}

.doctor-card {
  background: rgba(255, 255, 255, 0.95);
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.doctor-details h2 {
  color: #333;
  margin-bottom: 15px;
  font-size: 24px;
}

.doctor-details p {
  color: #666;
  margin: 8px 0;
  font-size: 15px;
}

/* Back Button */
.back-btn {
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #667eea;
  color: #667eea;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 25px;
  transition: all 0.3s;
}

.back-btn:hover {
  background: #667eea;
  color: white;
  transform: translateX(-5px);
}

/* Slots Section */
.slots-section {
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.slots-section h3 {
  color: #333;
  margin-bottom: 25px;
  font-size: 20px;
}

.slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* Slot Card */
.slot-card {
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px;
  background: white;
  transition: all 0.3s;
  text-align: center;
  min-height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.slot-card.available {
  border-color: #4caf50;
  background: #f1f8f4;
}

.slot-card.available:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(76, 175, 80, 0.3);
}

.slot-card.unavailable {
  border-color: #f44336;
  background: #fef5f5;
  opacity: 0.8;
}

.slot-card.booked {
  border-color: #ff9800;
  background: #fff8f0;
}

/* Slot Date */
.slot-date {
  margin-bottom: 15px;
}

.date-number {
  font-size: 32px;
  font-weight: bold;
  color: #667eea;
  line-height: 1;
}

.date-month {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
  margin: 5px 0;
}

.day-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-top: 5px;
}

/* Slot Content */
.slot-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.slot-time {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.slot-status {
  display: flex;
  justify-content: center;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.available {
  background: #c8e6c9;
  color: #2e7d32;
}

.status-badge.unavailable {
  background: #ffcdd2;
  color: #c62828;
}

.status-badge.open {
  background: #bbdefb;
  color: #1565c0;
}

.status-badge.booked {
  background: #ffe0b2;
  color: #e65100;
}

/* Buttons */
.book-btn,
.cancel-btn {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.book-btn {
  background: #4caf50;
  color: white;
}

.book-btn:hover {
  background: #45a049;
  transform: scale(1.02);
}

.book-btn:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
  transform: none;
}

.cancel-btn {
  background: #ff6b6b;
  color: white;
}

.cancel-btn:hover {
  background: #ff5252;
  transform: scale(1.02);
}

.cancel-btn:disabled {
  background: #bdbdbd;
  cursor: not-allowed;
  transform: none;
}

.booked-by-other {
  font-size: 12px;
  color: #ff6b6b;
  font-style: italic;
  padding: 8px;
  background: #fff0f0;
  border-radius: 4px;
}

/* Messages */
.loading,
.no-data {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 16px;
}

.warning-message {
  background: #fff3cd;
  border: 2px solid #ffc107;
  border-radius: 5px;
  padding: 20px;
  text-align: center;
  margin-bottom: 30px;
}

.warning-message p {
  color: #856404;
  margin: 0 0 15px 0;
  font-size: 15px;
}

.profile-link {
  display: inline-block;
  background: #ffc107;
  color: #856404;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.profile-link:hover {
  background: #ff9800;
  color: white;
  transform: scale(1.05);
}

.success-message,
.error-message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  z-index: 1000;
  animation: slideIn 0.3s ease-in;
}

.success-message {
  background: #4caf50;
  color: white;
}

.error-message {
  background: #f44336;
  color: white;
}

.close-msg {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
}

@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .appointment-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .appointment-header h1 {
    font-size: 22px;
  }

  .slots-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 15px;
  }

  .slot-card {
    min-height: 240px;
    padding: 15px;
  }

  .date-number {
    font-size: 28px;
  }

  .success-message,
  .error-message {
    width: calc(100% - 40px);
    right: 20px;
    left: 20px;
  }
}
</style>
