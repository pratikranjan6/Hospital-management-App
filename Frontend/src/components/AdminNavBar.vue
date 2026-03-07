<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Hospital Admin</a>
      
      <div class="d-flex flex-grow-1 justify-content-center">
        <form class="d-flex" @submit.prevent="handleSearch">
          <input 
            v-model="searchQuery" 
            class="form-control me-2" 
            type="search" 
            placeholder="Search doctors, patients, departments..."
            aria-label="Search"
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
      </div>

      <div class="navbar-nav ms-auto">
        <button @click="goToDashboard" class="nav-link btn btn-link text-white me-2">Dashboard</button>
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

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .search-bar {
    max-width: 100%;
  }

  .navbar-menu {
    width: 100%;
    justify-content: space-between;
  }
}
</style>
