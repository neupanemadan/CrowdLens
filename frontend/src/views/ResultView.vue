<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useDetectionStore } from '@/stores'
import DetectionResult from '@/components/detection/DetectionResult.vue'

const store = useDetectionStore()
const router = useRouter()

if (!store.currentDetection) {
  router.replace({ name: 'upload' })
}
</script>

<template>
  <div class="result-view">
    <div class="result-header">
      <h1>Detection Result</h1>
      <button class="back-btn" @click="router.push({ name: 'upload' })">Upload Another</button>
    </div>

    <DetectionResult v-if="store.currentDetection" :detection="store.currentDetection" />
  </div>
</template>

<style scoped>
.result-view {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h1 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: none;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  color: #475569;
  cursor: pointer;
  font-size: 0.85rem;
}

.back-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}
</style>
