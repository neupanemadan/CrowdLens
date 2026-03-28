<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDetectionStore } from '@/stores'
import DetectionTable from '@/components/detection/DetectionTable.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppError from '@/components/common/AppError.vue'

const store = useDetectionStore()
const router = useRouter()

onMounted(() => {
  store.fetchDetections()
})

function onSelect(id: number) {
  router.push({ name: 'detail', params: { id } })
}
</script>

<template>
  <div class="history-view">
    <h1>Detection History</h1>

    <AppLoader v-if="store.isLoading" text="Loading history..." />
    <AppError v-else-if="store.error" :message="store.error" />
    <DetectionTable v-else :detections="store.detections" @select="onSelect" />
  </div>
</template>

<style scoped>
.history-view {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

h1 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0;
}
</style>
