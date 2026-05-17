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
          <button class="btn-search" type="submit">Search</button>
        </form>
      </div>

      <div class="navbar-nav ms-auto">
        <button @click="goToDashboard" class="nav-link btn btn-link me-2">Dashboard</button>
        <button @click="logout" class="btn-logout">Logout</button>
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
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  background: #fffdf7 !important;
  border-bottom: 2px solid #d8c8b0;
}

.navbar-brand {
  font-size: 1.4rem;
  font-weight: 800;
  color: #8f7b65 !important;
  margin-right: 2rem;
  letter-spacing: -0.02em;
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
  border: 2px solid #d8c8b0;
  border-radius: 16px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  background: #fff9f1;
  color: #3d362f;
}

.search-input:focus {
  outline: none;
  border-color: #8f7b65;
  box-shadow: 0 0 0 3px rgba(143, 123, 101, 0.15);
  background: #fffdf7;
}

.search-input::placeholder {
  color: #bfafa1;
}

.nav-link {
  color: #3d362f !important;
  font-weight: 700;
  transition: all 0.3s ease;
  padding: 0.5rem 1rem !important;
}

.nav-link:hover {
  color: #8f7b65 !important;
}

.btn-search {
  padding: 0.75rem 1.5rem;
  background: #8f7b65;
  color: white;
  border: none;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-search:hover {
  background: #7a6a58;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.3);
}

.btn-logout {
  padding: 0.75rem 1.5rem;
  background: transparent;
  color: #8f7b65;
  border: 2px solid #8f7b65;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-logout:hover {
  background: #8f7b65;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(143, 123, 101, 0.3);
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
