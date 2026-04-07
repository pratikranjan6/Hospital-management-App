<template>
  <div class="profile-wrapper">
    <div class="profile-container">
      <!-- Welcome Header -->
      <div class="welcome-section">
        <div class="welcome-content">
          <h1 class="welcome-title">Edit Your Profile</h1>
          <p class="welcome-subtitle">Update your personal and medical information</p>
          <button @click="goBack" class="back-btn-header">
            <i class="fas fa-chevron-left"></i> Back
          </button>
        </div>
      </div>

      <!-- Profile Form Card -->
      <div class="profile-card">
        <div class="card-header">
          <div class="header-content">
            <h2 class="card-title">
              <i class="fas fa-user-circle"></i> Patient Information
            </h2>
            <p class="card-subtitle">Complete your medical profile</p>
          </div>
        </div>

        <div class="card-body">
          <div v-if="isLoading" class="loading-state">
            <div class="spinner"></div>
            <p>Loading profile...</p>
          </div>

          <form v-else @submit.prevent="saveProfile" class="profile-form">
            <!-- Name Field -->
            <div class="form-group">
              <label for="name" class="form-label">
                <i class="fas fa-user"></i> Full Name <span class="required">*</span>
              </label>
              <input
                id="name"
                v-model="profileForm.name"
                type="text"
                class="form-input"
                :class="{'has-error': formErrors.name}"
                placeholder="Enter your full name"
                required
              />
              <div v-if="formErrors.name" class="error-message">
                <i class="fas fa-exclamation-circle"></i> {{ formErrors.name }}
              </div>
            </div>

            <div class="form-row two-columns">
              <div class="form-group">
                <label for="age" class="form-label">
                  <i class="fas fa-birthday-cake"></i> Age <span class="required">*</span>
                </label>
                <input
                  id="age"
                  v-model.number="profileForm.age"
                  type="number"
                  min="0"
                  max="150"
                  class="form-input"
                  :class="{'has-error': formErrors.age}"
                  placeholder="Enter your age"
                  required
                />
                <div v-if="formErrors.age" class="error-message">
                  <i class="fas fa-exclamation-circle"></i> {{ formErrors.age }}
                </div>
              </div>

              <div class="form-group">
                <label for="dob" class="form-label">
                  <i class="fas fa-calendar"></i> Date of Birth <span class="required">*</span>
                </label>
                <input
                  id="dob"
                  v-model="profileForm.date_of_birth"
                  type="date"
                  class="form-input"
                  :class="{'has-error': formErrors.date_of_birth}"
                  required
                />
                <div v-if="formErrors.date_of_birth" class="error-message">
                  <i class="fas fa-exclamation-circle"></i> {{ formErrors.date_of_birth }}
                </div>
              </div>
            </div>

            <!-- Gender and Blood Group Row -->
            <div class="form-row two-columns">
              <div class="form-group">
                <label for="gender" class="form-label">
                  <i class="fas fa-mars-and-venus"></i> Gender <span class="required">*</span>
                </label>
                <select
                  id="gender"
                  v-model="profileForm.gender"
                  class="form-input"
                  :class="{'has-error': formErrors.gender}"
                  required
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
                <div v-if="formErrors.gender" class="error-message">
                  <i class="fas fa-exclamation-circle"></i> {{ formErrors.gender }}
                </div>
              </div>

              <div class="form-group">
                <label for="blood_group" class="form-label">
                  <i class="fas fa-droplet"></i> Blood Group <span class="required">*</span>
                </label>
                <select
                  id="blood_group"
                  v-model="profileForm.blood_group"
                  class="form-input"
                  :class="{'has-error': formErrors.blood_group}"
                  required
                >
                  <option value="">Select Blood Group</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                </select>
                <div v-if="formErrors.blood_group" class="error-message">
                  <i class="fas fa-exclamation-circle"></i> {{ formErrors.blood_group }}
                </div>
              </div>
            </div>

            <!-- Address Field -->
            <div class="form-group">
              <label for="address" class="form-label">
                <i class="fas fa-map-marker-alt"></i> Address
              </label>
              <textarea
                id="address"
                v-model="profileForm.address"
                class="form-input textarea-input"
                rows="4"
                placeholder="Enter your address"
              ></textarea>
              <div v-if="formErrors.address" class="error-message">
                <i class="fas fa-exclamation-circle"></i> {{ formErrors.address }}
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="form-actions">
              <button
                type="submit"
                class="btn-primary"
                :disabled="isSaving"
              >
                <i class="fas fa-save"></i>
                {{ isSaving ? 'Saving...' : 'Save Changes' }}
              </button>
              <button
                type="button"
                @click="resetForm"
                class="btn-secondary"
                :disabled="isSaving"
              >
                <i class="fas fa-redo"></i> Reset
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Success Notification -->
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

    <!-- Error Notification -->
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
  name: 'EditProfile',
  data() {
    return {
      profileForm: {
        name: '',
        age: null,
        date_of_birth: '',
        gender: '',
        blood_group: '',
        address: ''
      },
      originalProfile: {},
      formErrors: {},
      isSaving: false,
      isLoading: true,
      successMessage: '',
      errorMessage: ''
    }
  },
  mounted() {
    this.fetchPatientProfile()
  },
  methods: {
    async fetchPatientProfile() {
      try {
        this.isLoading = true
        const response = await fetch(`${getApiBase()}/api/patient/profile`, {
          method: 'GET',
          headers: getAuthHeader()
        })

        if (!response.ok) {
          throw new Error('Failed to fetch profile')
        }

        const data = await response.json()
        
        this.profileForm = {
          name: data.name || '',
          age: data.age || null,
          date_of_birth: data.date_of_birth || '',
          gender: data.gender || '',
          blood_group: data.blood_group || '',
          address: data.address || ''
        }

        this.originalProfile = { ...this.profileForm }
      } catch (error) {
        console.error('Error fetching profile:', error)
        this.errorMessage = 'Failed to load profile. Please try again.'
      } finally {
        this.isLoading = false
      }
    },

    validateForm() {
      this.formErrors = {}
      let isValid = true

      if (!this.profileForm.name || this.profileForm.name.trim() === '') {
        this.formErrors.name = 'Name is required'
        isValid = false
      } else if (this.profileForm.name.length < 2) {
        this.formErrors.name = 'Name must be at least 2 characters'
        isValid = false
      }

      if (this.profileForm.age === null || this.profileForm.age === '') {
        this.formErrors.age = 'Age is required'
        isValid = false
      } else if (this.profileForm.age < 0 || this.profileForm.age > 150) {
        this.formErrors.age = 'Age must be between 0 and 150'
        isValid = false
      }

      if (!this.profileForm.date_of_birth) {
        this.formErrors.date_of_birth = 'Date of birth is required'
        isValid = false
      } else {
        const dob = new Date(this.profileForm.date_of_birth)
        const today = new Date()
        if (dob > today) {
          this.formErrors.date_of_birth = 'Date of birth cannot be in the future'
          isValid = false
        }
      }

      if (!this.profileForm.gender) {
        this.formErrors.gender = 'Gender is required'
        isValid = false
      }

      if (!this.profileForm.blood_group) {
        this.formErrors.blood_group = 'Blood group is required'
        isValid = false
      }

      return isValid
    },

    async saveProfile() {
      if (!this.validateForm()) {
        this.errorMessage = 'Please fix the errors in the form'
        return
      }

      try {
        this.isSaving = true
        this.errorMessage = ''
        this.successMessage = ''

        const profileData = {
          name: this.profileForm.name,
          age: this.profileForm.age,
          date_of_birth: this.profileForm.date_of_birth,
          gender: this.profileForm.gender,
          blood_group: this.profileForm.blood_group,
          address: this.profileForm.address
        }

        const response = await fetch(`${getApiBase()}/api/patient/profile`, {
          method: 'POST',
          headers: {
            ...getAuthHeader(),
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(profileData)
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.msg || 'Failed to save profile')
        }

        const result = await response.json()
        
        this.originalProfile = { ...this.profileForm }
        
        this.successMessage = result.msg || 'Profile saved successfully!'
        
        setTimeout(() => {
          this.successMessage = ''
        }, 3000)
      } catch (error) {
        console.error('Error saving profile:', error)
        this.errorMessage = error.message || 'Failed to save profile. Please try again.'
      } finally {
        this.isSaving = false
      }
    },

    resetForm() {
      this.profileForm = { ...this.originalProfile }
      this.formErrors = {}
      this.errorMessage = ''
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

.profile-wrapper {
  width: 100%;
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.profile-container {
  flex: 1;
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

/* ========== ANIMATIONS ========== */
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

/* ========== WELCOME SECTION ========== */
.welcome-section {
  margin-bottom: 2.5rem;
  animation: slideDown 0.5s ease-out;
}

.welcome-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.welcome-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.welcome-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
  margin: 0;
}

.back-btn-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
  white-space: nowrap;
}

.back-btn-header:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

/* ========== PROFILE CARD ========== */
.profile-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border-top: 4px solid #667eea;
  animation: cardSlide 0.5s ease-out;
}

.profile-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-title i {
  color: #667eea;
  font-size: 1.5rem;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin: 0;
}

.card-body {
  padding: 2rem;
}

/* ========== LOADING STATE ========== */
.loading-state {
  text-align: center;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #7f8c8d;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f0f0f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* ========== FORM STYLES ========== */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-label i {
  color: #667eea;
  font-size: 1rem;
}

.required {
  color: #e74c3c;
  font-weight: 700;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  color: #2c3e50;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #f9f9f9;
}

.form-input:hover {
  border-color: #667eea;
  background: #fff;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input.has-error {
  border-color: #e74c3c;
  background: #fff5f5;
}

.form-input.has-error:focus {
  box-shadow: 0 0 0 3px rgba(231, 76, 60, 0.1);
}

.textarea-input {
  resize: vertical;
  min-height: 100px;
}

/* ========== FORM ROW ========== */
.form-row {
  display: flex;
  gap: 1.5rem;
}

.two-columns {
  grid-template-columns: repeat(2, 1fr);
}

.form-row .form-group {
  flex: 1;
}

/* ========== ERROR MESSAGE ========== */
.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #e74c3c;
  animation: slideUp 0.3s ease-out;
}

.error-message i {
  font-size: 0.9rem;
}

/* ========== ACTION BUTTONS ========== */
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e0e0e0;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex: 1;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 1.5px solid #667eea;
}

.btn-secondary:hover:not(:disabled) {
  background: #e8eef7;
  transform: translateY(-2px);
}

.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* ========== NOTIFICATIONS ========== */
.notification {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  max-width: 420px;
  border-radius: 10px;
  padding: 1.25rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease;
  z-index: 1000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(400px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.success-notification {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  border: 1px solid #6ee7b7;
}

.error-notification {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 1px solid #fca5a5;
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
  color: #10b981;
}

.error-notification i {
  color: #ef4444;
}

.notification-title {
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.success-notification .notification-title {
  color: #166534;
}

.error-notification .notification-title {
  color: #991b1b;
}

.notification-message {
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.85;
}

.success-notification .notification-message {
  color: #166534;
}

.error-notification .notification-message {
  color: #991b1b;
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
  color: #10b981;
}

.error-notification .notification-close {
  color: #ef4444;
}

.notification-close:hover {
  transform: scale(1.2);
}

/* ========== RESPONSIVE DESIGN ========== */
@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }

  .welcome-content {
    flex-direction: column;
    padding: 1.5rem;
    text-align: center;
  }

  .welcome-title {
    font-size: 1.5rem;
  }

  .back-btn-header {
    width: 100%;
  }

  .card-body {
    padding: 1.5rem;
  }

  .form-row {
    flex-direction: column;
  }

  .form-row.two-columns {
    gap: 1rem;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .notification {
    right: 1rem;
    left: 1rem;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .profile-container {
    padding: 0.75rem;
  }

  .welcome-content {
    padding: 1rem;
  }

  .welcome-title {
    font-size: 1.2rem;
  }

  .welcome-subtitle {
    font-size: 0.85rem;
  }

  .card-body {
    padding: 1rem;
  }

  .card-title {
    font-size: 1.1rem;
  }

  .form-label {
    font-size: 0.9rem;
  }

  .form-input {
    padding: 0.65rem 0.75rem;
    font-size: 0.9rem;
  }

  .form-actions {
    gap: 0.5rem;
  }

  .btn-primary,
  .btn-secondary {
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
    gap: 0.5rem;
  }

  .notification {
    top: 1rem;
    right: 0.5rem;
    left: 0.5rem;
    font-size: 0.85rem;
  }
}
</style>