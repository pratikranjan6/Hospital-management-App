<template>
  <nav class="admin-navbar">
    <div class="navbar-container">
      <div class="navbar-logo">
        <h1>Hospital Admin</h1>
      </div>
      
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search doctors, patients, departments..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="btn-search">Search</button>
      </div>

      <div class="navbar-menu">
        <button @click="goToDashboard" class="nav-link">Dashboard</button>
        <button @click="logout" class="nav-link logout">Logout</button>
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
  // Navigate to dashboard with search query; dashboard will perform the backend call
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
.admin-navbar {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  gap: 2rem;
}

.navbar-logo h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  white-space: nowrap;
}

.search-bar {
  display: flex;
  gap: 0.5rem;
  flex: 1;
  max-width: 400px;
}

.search-bar input {
  flex: 1;
  padding: 0.6rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}

.search-bar input:focus {
  box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.2);
}

.btn-search {
  padding: 0.6rem 1.2rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s ease;
  white-space: nowrap;
}

.btn-search:hover {
  background-color: #45a049;
}

.navbar-menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  background: transparent;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 4px;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.logout {
  background-color: #e74c3c;
}

.nav-link.logout:hover {
  background-color: #c0392b;
}

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
