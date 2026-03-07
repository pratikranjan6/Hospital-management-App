<template>
  <div class="history">
    <div class="history-header">
      <h1>History</h1>
      <button @click="goBack" class="back-btn">← Back</button>
    </div>
    <div class="history-content">
      <p>Patient history feature coming soon...</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'History',
  methods: {
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>
.history {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.history-header h1 {
  margin: 0;
  font-size: 28px;
  color: #333;
  font-weight: 600;
}

.back-btn {
  padding: 8px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #5a6268;
}

.history-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
