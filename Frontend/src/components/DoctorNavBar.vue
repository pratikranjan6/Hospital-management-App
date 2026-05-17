<template>
  <nav class="custom-navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <span class="brand-text">Dr. {{ username }}</span>
      </div>

      <div class="navbar-center">
        <button @click="goDashboard" class="nav-link"> Dashboard</button>
        <button @click="goAvailability" class="nav-link"> Availability</button>
      </div>

      <div class="navbar-actions">
        <button @click="logout" class="btn-logout">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref(localStorage.getItem('username') || 'Doctor')

function goDashboard() {
  router.push('/doctor_dashboard')
}

function goAvailability() {
  router.push('/doctor_availability')
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('role')
  router.push('/login')
}
</script>

<style scoped>
.custom-navbar {
  width: 100%;
  background: #fffdf7;
  border-bottom: 2px solid #d8c8b0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 2rem;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  gap: 2rem;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.brand-text {
  font-size: 1.3rem;
  font-weight: 800;
  color: #8f7b65;
  letter-spacing: -0.5px;
}

.navbar-center {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.nav-link {
  padding: 0.6rem 1.2rem;
  background: transparent;
  border: none;
  color: #3d362f;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 16px;
  font-size: 0.95rem;
  white-space: nowrap;
}

.nav-link:hover {
  background: #f4e9db;
  color: #8f7b65;
  transform: translateY(-2px);
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.btn-logout {
  padding: 0.65rem 1.5rem;
  background: #8f7b65;
  color: white;
  border: none;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.95rem;
}

.btn-logout:hover {
  transform: translateY(-2px);
  background: #7a6a58;
  box-shadow: 0 8px 20px rgba(143, 123, 101, 0.3);
}

.btn-logout:active {
  transform: translateY(0);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 1024px) {
  .navbar-center {
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.6rem 0.9rem;
    font-size: 0.9rem;
  }

  .navbar-container {
    padding: 1rem 1.5rem;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    flex-wrap: wrap;
    padding: 1rem;
    gap: 0.75rem;
  }

  .navbar-brand {
    order: 1;
    width: 100%;
  }

  .navbar-center {
    order: 2;
    width: 100%;
    justify-content: space-around;
    gap: 0.5rem;
  }

  .navbar-actions {
    order: 3;
    width: 100%;
    justify-content: flex-end;
  }

  .brand-text {
    font-size: 1.1rem;
  }

  .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }

  .btn-logout {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .navbar-container {
    flex-direction: column;
    padding: 0.75rem;
    gap: 0.5rem;
  }

  .navbar-brand {
    width: 100%;
    justify-content: flex-start;
  }

  .brand-icon {
    font-size: 1.5rem;
  }

  .brand-text {
    font-size: 1rem;
  }

  .navbar-center {
    width: 100%;
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.45rem 0.6rem;
    font-size: 0.75rem;
  }

  .navbar-actions {
    width: 100%;
  }

  .btn-logout {
    width: 100%;
    padding: 0.55rem 1rem;
    font-size: 0.85rem;
  }
}
</style>
