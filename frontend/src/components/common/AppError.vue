<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>

<template>
  <div class="error-box">
    <p>{{ message }}</p>
  </div>
</template>

<style scoped>
.error-box {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 1rem;
  color: #dc2626;
  font-size: 0.875rem;
}
</style>
