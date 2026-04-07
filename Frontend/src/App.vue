<script setup>
import FloatingAIButton from './components/FloatingAIButton.vue'
</script>

<template>
  <div class="page-container">
    <router-view />
    <FloatingAIButton />
  </div>
</template>

<style>
.page-container {
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  padding: 2rem;
  background-color: #edf2f7; /* match admin background */
  min-height: 100vh;
}
</style>