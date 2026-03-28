<script setup lang="ts">
const props = defineProps<{
  text?: string
}>()
</script>

<template>
  <div class="loading">
    <div class="spinner"></div>
    <p v-if="props.text">{{ props.text }}</p>
  </div>
</template>

<style scoped>
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #64748b;
  font-size: 0.875rem;
}
</style>
