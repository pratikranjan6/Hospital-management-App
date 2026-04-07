<template>
   <div class="content-wrapper">
      <!-- Navigation Header -->
      <nav class="navbar">
         <div class="nav-container">
            <!-- Logo on left -->
            <div class="logo-section">
               <div class="logo"> MediCare</div>
            </div>

            <!-- Auth buttons on right -->
            <div class="nav-buttons">
               <button @click="$router.push('/login')" class="nav-btn btn-login">
                  Login
               </button>
               <button @click="$router.push('/register')" class="nav-btn btn-signup">
                  Sign up
               </button>
            </div>
         </div>
      </nav>

      <!-- Hero Section with Logo and Description -->
      <section class="hero-section">
         <div class="hero-content">
            <div class="hero-logo"></div>
            <h1 class="hero-title">HealthFirst Platform</h1>
            <p class="hero-subtitle">Advanced Healthcare Solution for Better Patient Care</p>
            
            <!-- Description replacing search bar -->
            <div class="description-box">
               <p class="desc-main">Experience the future of hospital management with our comprehensive, integrated healthcare platform.</p>
               <p class="desc-secondary">Seamlessly manage patient records, doctor schedules, departments, and appointments all in one unified system for enhanced efficiency and better patient outcomes.</p>
            </div>

            <!-- CTA Button -->
            <div class="cta-section">
               <button @click="$router.push('/login')" class="cta-btn">
                  Get Started ⮕
               </button>
            </div>
         </div>
      </section>

      <!-- Statistics Section -->
      <section class="stats-section">
         <div class="stats-container">
            <!-- Departments Card -->
            <div class="stat-card">
               <div class="stat-icon departments-icon"></div>
               <div class="stat-content">
                  <div class="stat-number">{{ stats.departments }}</div>
                  <div class="stat-label">Total Departments</div>
               </div>
            </div>

            <!-- Doctors Card -->
            <div class="stat-card">
               <div class="stat-icon doctors-icon"></div>
               <div class="stat-content">
                  <div class="stat-number">{{ stats.doctors }}</div>
                  <div class="stat-label">Active Doctors</div>
               </div>
            </div>

            <!-- Patients Card -->
            <div class="stat-card">
               <div class="stat-icon patients-icon"></div>
               <div class="stat-content">
                  <div class="stat-number">{{ stats.patients }}</div>
                  <div class="stat-label">Total Patients</div>
               </div>
            </div>
         </div>
      </section>
   </div>
</template>

<script>
import axios from 'axios';

export default {
   name: 'Content',
   data() {
      return {
         stats: {
            departments: 0,
            doctors: 0,
            patients: 0
         }
      }
   },
   mounted() {
      this.fetchStats();
   },
   methods: {
      async fetchStats() {
         try {
            const token = localStorage.getItem('access_token');
            if (!token) {
               // If no token, show default stats
               this.stats = { departments: 0, doctors: 0, patients: 0 };
               return;
            }

            const headers = { Authorization: `Bearer ${token}` };

            // Fetch departments
            const deptRes = await axios.get('http://127.0.0.1:5000/api/departments', { headers });
            this.stats.departments = deptRes.data.length;

            // Fetch doctors
            const docRes = await axios.get('http://127.0.0.1:5000/api/admin/doctors', { headers });
            this.stats.doctors = docRes.data.length;

            // Fetch patients
            const patRes = await axios.get('http://127.0.0.1:5000/api/admin/patients', { headers });
            this.stats.patients = patRes.data.length;
         } catch (error) {
            console.error('Error fetching statistics:', error);
            // Keep default values on error
         }
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

.content-wrapper {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* ========== NAVBAR ========== */
.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #007bff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: color 0.3s ease;
}

.logo:hover {
  color: #0056b3;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  padding: 0.6rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-login {
  background: transparent;
  color: #333;
  border: 2px solid #333;
}

.btn-login:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
}

.btn-signup {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.btn-signup:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* ========== HERO SECTION ========== */
.hero-section {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-content {
  max-width: 700px;
  width: 100%;
  animation: fadeInDown 0.8s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-logo {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2rem;
  font-weight: 300;
}

.description-box {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-bottom: 2rem;
  border-top: 4px solid #667eea;
}

.desc-main {
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.desc-secondary {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.7;
  margin: 0;
}

.cta-section {
  margin-bottom: 3rem;
}

.cta-btn {
  padding: 1rem 2.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.cta-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.cta-btn:active {
  transform: translateY(-1px);
}

/* ========== STATS SECTION ========== */
.stats-section {
  background: white;
  padding: 4rem 2rem;
  border-top: 1px solid #e0e0e0;
}

.stats-container {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.stat-card:nth-child(1) {
  border-left: 5px solid #667eea;
}

.stat-card:nth-child(2) {
  border-left: 5px solid #764ba2;
}

.stat-card:nth-child(3) {
  border-left: 5px solid #f093fb;
}

.stat-icon {
  font-size: 3rem;
  min-width: 70px;
  text-align: center;
  animation: iconFloat 3s ease-in-out infinite;
}

.stat-icon.departments-icon {
  animation-delay: 0s;
}

.stat-icon.doctors-icon {
  animation-delay: 0.5s;
}

.stat-icon.patients-icon {
  animation-delay: 1s;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  color: #666;
  font-weight: 500;
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
  }

  .logo {
    font-size: 1.2rem;
  }

  .nav-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .hero-section {
    padding: 2rem 1rem;
  }

  .hero-logo {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
    margin-bottom: 1.5rem;
  }

  .description-box {
    padding: 1.5rem;
    margin-bottom: 1.5rem;
  }

  .desc-main {
    font-size: 1rem;
  }

  .desc-secondary {
    font-size: 0.9rem;
  }

  .cta-btn {
    padding: 0.8rem 2rem;
    font-size: 0.95rem;
  }

  .stats-section {
    padding: 2rem 1rem;
  }

  .stats-container {
    gap: 1rem;
  }

  .stat-card {
    gap: 1rem;
    padding: 1.5rem;
  }

  .stat-icon {
    font-size: 2.5rem;
    min-width: 60px;
  }

  .stat-number {
    font-size: 2rem;
  }

  .stat-label {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .nav-buttons {
    gap: 0.5rem;
  }

  .nav-btn {
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
  }

  .hero-title {
    font-size: 1.5rem;
  }

  .hero-subtitle {
    font-size: 0.9rem;
  }

  .description-box {
    padding: 1rem;
  }

  .desc-main {
    font-size: 0.95rem;
  }

  .desc-secondary {
    font-size: 0.85rem;
  }

  .stat-card {
    flex-direction: column;
    text-align: center;
  }

  .stat-number {
    font-size: 1.8rem;
  }

  .stat-label {
    font-size: 0.85rem;
  }
}
</style>
