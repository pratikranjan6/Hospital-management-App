<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Hospital Admin</a>
      
      <div class="search-container">
        <form class="search-form" @submit.prevent="handleSearch">
          <input 
            v-model="searchQuery" 
            class="search-input" 
            type="search" 
            placeholder="Search doctors, patients, departments..."
            aria-label="Search"
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>

      <div class="navbar-nav ms-auto">
        <button @click="goToDashboard" class="nav-link btn btn-link me-2">Dashboard</button>
        <button @click="logout" class="btn btn-outline-danger">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { getApiBase, getAuthHeader } from '../utils/auth'

const router = useRouter()
const API_BASE = getApiBase()
const searchQuery = ref('')

async function handleSearch() {
  if (!searchQuery.value.trim()) {
    router.push('/admin_dashboard')
    return
  }
  router.push({ path: '/admin_dashboard', query: { search: searchQuery.value } })
}

function goToDashboard() {
  searchQuery.value = ''
  router.push('/admin_dashboard')
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  router.push('/login')
}
</script>
<style scoped>
.custom-navbar {
  padding: 1.5rem 0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background: white !important;
  border-bottom: 1px solid #e0e0e0;
}

.navbar-brand {
  font-size: 1.4rem;
  font-weight: 700;
  color: #667eea !important;
  margin-right: 2rem;
}

.search-container {
  flex-grow: 1;
  display: flex;
  justify-content: flex-start;
  padding: 0 1rem;
}

.search-form {
  display: flex;
  gap: 0.5rem;
  width: 100%;
  max-width: 500px;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #28a745;
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
}

.nav-link {
  color: #2c3e50 !important;
  font-weight: 600;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem !important;
}

.nav-link:hover {
  color: #667eea !important;
}

@media (max-width: 768px) {
  .search-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .search-form {
    max-width: 100%;
  }

  .navbar-menu {
    width: 100%;
    justify-content: space-between;
  }

  .custom-navbar {
    padding: 1rem 0 !important;
  }
}
</style>
