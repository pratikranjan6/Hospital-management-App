<template>
  <div class="edit-profile">
    <div class="profile-header">
      <h1>Edit Profile</h1>
      <div class="header-actions">
        <router-link to="/user_dashboard" class="action-link">Dashboard</router-link>
        <span class="divider">|</span>
        <button @click="logout" class="logout-btn">logout</button>
      </div>
    </div>

    <button @click="goBack" class="back-btn">← Back</button>

    <div class="profile-form-container">
      <div class="form-wrapper">
        <h2>Patient Information</h2>
        
        <form @submit.prevent="saveProfile" class="profile-form">
          <div class="form-group">
            <label for="name">Full Name <span class="required">*</span></label>
            <input
              id="name"
              v-model="profileForm.name"
              type="text"
              class="form-input"
              placeholder="Enter your full name"
              required
            />
            <span v-if="formErrors.name" class="error-message">{{ formErrors.name }}</span>
          </div>

          <div class="form-group">
            <label for="age">Age <span class="required">*</span></label>
            <input
              id="age"
              v-model.number="profileForm.age"
              type="number"
              min="0"
              max="150"
              class="form-input"
              placeholder="Enter your age"
              required
            />
            <span v-if="formErrors.age" class="error-message">{{ formErrors.age }}</span>
          </div>

          <div class="form-group">
            <label for="dob">Date of Birth <span class="required">*</span></label>
            <input
              id="dob"
              v-model="profileForm.date_of_birth"
              type="date"
              class="form-input"
              required
            />
            <span v-if="formErrors.date_of_birth" class="error-message">{{ formErrors.date_of_birth }}</span>
          </div>

          <div class="form-group">
            <label for="gender">Gender <span class="required">*</span></label>
            <select
              id="gender"
              v-model="profileForm.gender"
              class="form-input"
              required
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
            <span v-if="formErrors.gender" class="error-message">{{ formErrors.gender }}</span>
          </div>

          <div class="form-group">
            <label for="blood_group">Blood Group <span class="required">*</span></label>
            <select
              id="blood_group"
              v-model="profileForm.blood_group"
              class="form-input"
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
            <span v-if="formErrors.blood_group" class="error-message">{{ formErrors.blood_group }}</span>
          </div>

          <div class="form-group">
            <label for="address">Address</label>
            <textarea
              id="address"
              v-model="profileForm.address"
              class="form-textarea"
              rows="3"
              placeholder="Enter your address"
            ></textarea>
            <span v-if="formErrors.address" class="error-message">{{ formErrors.address }}</span>
          </div>

          <div class="form-actions">
            <button
              type="submit"
              class="save-btn"
              :disabled="isSaving"
            >
              {{ isSaving ? 'Saving...' : 'Save Profile' }}
            </button>
            <button
              type="button"
              @click="resetForm"
              class="reset-btn"
              :disabled="isSaving"
            >
              Reset
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
      <button @click="successMessage = ''" class="close-msg">&times;</button>
    </div>

    <div v-if="errorMessage" class="error-alert">
      {{ errorMessage }}
      <button @click="errorMessage = ''" class="close-msg">&times;</button>
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

.edit-profile {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header */
.profile-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-header h1 {
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

/* Form Container */
.profile-form-container {
  max-width: 700px;
  margin: 0 auto;
}

.form-wrapper {
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-wrapper h2 {
  color: #333;
  margin-bottom: 30px;
  font-size: 24px;
}

/* Form Groups */
.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 600;
  font-size: 15px;
}

.required {
  color: #f44336;
}

.form-input,
.form-textarea {
  width: 100%;
  color:#333;
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.3s;
  background: white;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #999;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.error-message {
  display: block;
  color: #f44336;
  font-size: 13px;
  margin-top: 5px;
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 15px;
  margin-top: 35px;
}

.save-btn,
.reset-btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.save-btn {
  background: #667eea;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #764ba2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.reset-btn {
  background: #f5f5f5;
  color: #333;
  border: 2px solid #ddd;
}

.reset-btn:hover:not(:disabled) {
  background: #e0e0e0;
  border-color: #999;
}

.save-btn:disabled,
.reset-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Messages */
.success-message,
.error-alert {
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

.error-alert {
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
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .profile-header h1 {
    font-size: 22px;
  }

  .form-wrapper {
    padding: 25px;
  }

  .form-actions {
    flex-direction: column;
  }

  .save-btn,
  .reset-btn {
    width: 100%;
  }

  .success-message,
  .error-alert {
    width: calc(100% - 40px);
    right: 20px;
    left: 20px;
  }
}
</style>