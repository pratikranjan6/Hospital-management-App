<template>
  <div class="container-fluid py-4">
    <div class="card mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center">
          <h2 class="h3 mb-0">Edit Profile</h2>
        </div>
      </div>
    </div>

    <button @click="goBack" class="btn btn-secondary mb-4">← Back</button>

    <div class="row justify-content-center">
      <div class="col-12">
        <div class="card">
          <div class="card-body">
            <h2 class="h4 mb-4">Patient Information</h2>
            
            <form @submit.prevent="saveProfile">
              <div class="mb-3">
                <label for="name" class="form-label">Full Name <span class="text-danger">*</span></label>
                <input
                  id="name"
                  v-model="profileForm.name"
                  type="text"
                  class="form-control"
                  :class="{'is-invalid': formErrors.name}"
                  placeholder="Enter your full name"
                  required
                />
                <div v-if="formErrors.name" class="invalid-feedback">
                  {{ formErrors.name }}
                </div>
              </div>

              <div class="mb-3">
                <label for="age" class="form-label">Age <span class="text-danger">*</span></label>
                <input
                  id="age"
                  v-model.number="profileForm.age"
                  type="number"
                  min="0"
                  max="150"
                  class="form-control"
                  :class="{'is-invalid': formErrors.age}"
                  placeholder="Enter your age"
                  required
                />
                <div v-if="formErrors.age" class="invalid-feedback">
                  {{ formErrors.age }}
                </div>
              </div>

              <div class="mb-3">
                <label for="dob" class="form-label">Date of Birth <span class="text-danger">*</span></label>
                <input
                  id="dob"
                  v-model="profileForm.date_of_birth"
                  type="date"
                  class="form-control"
                  :class="{'is-invalid': formErrors.date_of_birth}"
                  required
                />
                <div v-if="formErrors.date_of_birth" class="invalid-feedback">
                  {{ formErrors.date_of_birth }}
                </div>
              </div>

              <div class="mb-3">
                <label for="gender" class="form-label">Gender <span class="text-danger">*</span></label>
                <select
                  id="gender"
                  v-model="profileForm.gender"
                  class="form-select"
                  :class="{'is-invalid': formErrors.gender}"
                  required
                >
                  <option value="">Select Gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
                <div v-if="formErrors.gender" class="invalid-feedback">
                  {{ formErrors.gender }}
                </div>
              </div>

              <div class="mb-3">
                <label for="blood_group" class="form-label">Blood Group <span class="text-danger">*</span></label>
                <select
                  id="blood_group"
                  v-model="profileForm.blood_group"
                  class="form-select"
                  :class="{'is-invalid': formErrors.blood_group}"
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
                <div v-if="formErrors.blood_group" class="invalid-feedback">
                  {{ formErrors.blood_group }}
                </div>
              </div>

              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea
                  id="address"
                  v-model="profileForm.address"
                  class="form-control"
                  rows="3"
                  placeholder="Enter your address"
                ></textarea>
                <div v-if="formErrors.address" class="invalid-feedback">
                  {{ formErrors.address }}
                </div>
              </div>

              <div class="d-grid gap-2 d-md-flex">
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="isSaving"
                >
                  {{ isSaving ? 'Saving...' : 'Save Profile' }}
                </button>
                <button
                  type="button"
                  @click="resetForm"
                  class="btn btn-outline-secondary"
                  :disabled="isSaving"
                >
                  Reset
                </button>
              </div>
            </form>
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