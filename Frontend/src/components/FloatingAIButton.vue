<template>
  <div class="floating-ai-container">
    <button @click="isOpen = !isOpen" class="floating-ai-btn" :class="{ active: isOpen }">
      <span class="ai-badge">AI</span>
    </button>

    <AIAssistant :isOpen="isOpen" @close="isOpen = false" />
  </div>
</template>

<script>
import AIAssistant from './AIAssistant.vue'

export default {
  name: 'FloatingAIButton',
  components: { AIAssistant },
  data() {
    return {
      isOpen: false
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

.floating-ai-container {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
}

.floating-ai-btn {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #8f7b65 0%, #6d5f53 100%);
  color: white;
  border: none;
  font-size: 1.8rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(143, 123, 101, 0.4);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.floating-ai-btn:hover {
  transform: scale(1.1) translateY(-10px);
  box-shadow: 0 8px 30px rgba(143, 123, 101, 0.6);
}

.floating-ai-btn.active {
  animation: none;
  transform: scale(1.15);
  box-shadow: 0 8px 30px rgba(143, 123, 101, 0.8);
}

.gemini-logo {
  width: 45px;
  height: 45px;
  position: absolute;
}

.ai-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 800;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.4);
  animation: badgePulse 2s ease-in-out infinite;
}

@keyframes badgePulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .floating-ai-container {
    bottom: 1rem;
    right: 1rem;
  }

  .floating-ai-btn {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .ai-badge {
    width: 24px;
    height: 24px;
    font-size: 0.65rem;
    top: -8px;
    right: -8px;
  }
}

@media (max-width: 480px) {
  .floating-ai-container {
    bottom: 0.75rem;
    right: 0.75rem;
  }

  .floating-ai-btn {
    width: 55px;
    height: 55px;
    font-size: 1.3rem;
  }

  .ai-badge {
    width: 22px;
    height: 22px;
    font-size: 0.6rem;
  }
}
</style>
