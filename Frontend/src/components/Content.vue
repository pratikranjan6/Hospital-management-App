<template>
   <div class="content-container">
      <div class="content-page">
         <h1> Welcome to Hospital Management System</h1>
         <h2>Your Healthcare Solution</h2>
         
         <div class="description">
            <p>Experience efficient hospital management with our comprehensive healthcare system.</p>
            <p>Manage patients, appointments, staff, and resources - all in one integrated platform!</p>
         </div>

         <div class="action-section">
            <button @click="$router.push('/login')" class="btn btn-primary">
                Get Started ⮕
            </button>
         </div>
      </div>
   </div>
</template>

<script>
export default {
   name: 'Content'
}
</script>

<style scoped>
.content-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.content-page {
  max-width: 600px;
  width: 100%;
  background-color: #ffffff;
  padding: 3rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  text-align: center;
}

.content-page h1 {
  color: white;
  background-color: #324e6a;
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

.content-page h2 {
  color: white;
  background-color: #324e6a;
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.description {
  margin: 2rem 0;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.description p {
  color: #2c3e50;
  font-size: 1.1rem;
  line-height: 1.6;
  margin: 0.5rem 0;
}

.action-section {
  margin-top: 2rem;
}

.btn {
  padding: 0.875rem 2rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #667eea;
  color: white;
}

.btn-primary:hover {
  background-color: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}
</style>
