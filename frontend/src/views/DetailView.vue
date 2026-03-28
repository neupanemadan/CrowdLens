<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDetectionStore } from '@/stores'
import DetectionResult from '@/components/detection/DetectionResult.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppError from '@/components/common/AppError.vue'

const store = useDetectionStore()
const route = useRoute()
const router = useRouter()

onMounted(() => {
  const id = Number(route.params.id)
  if (id) store.fetchDetection(id)
})
</script>

<template>
  <div class="detail-view">
    <div class="detail-header">
      <h1>Detection Detail</h1>
      <button class="back-btn" @click="router.push({ name: 'history' })">Back to History</button>
    </div>

    <AppLoader v-if="store.isLoading" text="Loading..." />
    <AppError v-else-if="store.error" :message="store.error" />
    <DetectionResult v-else-if="store.currentDetection" :detection="store.currentDetection" />
  </div>
</template>

<style scoped>
.detail-view {
  max-width: 700px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.detail-header {
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
