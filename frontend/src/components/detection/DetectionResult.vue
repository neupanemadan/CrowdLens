<script setup lang="ts">
import type { Detection } from '@/types'

const props = defineProps<{
  detection: Detection
}>()

const mediaBase = import.meta.env.VITE_MEDIA_BASE_URL || 'http://localhost:8000'

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleString()
}
</script>

<template>
  <div class="result-card">
    <div class="result-image">
      <img
        :src="`${mediaBase}/media/${props.detection.annotated_image_path.replace('uploads/', '')}`"
        alt="Annotated"
      />
    </div>

    <div class="result-info">
      <div class="stat">
        <span class="stat-label">People Detected</span>
        <span class="stat-value">{{ props.detection.person_count }}</span>
      </div>

      <div class="meta">
        <p><strong>File:</strong> {{ props.detection.original_filename }}</p>
        <p><strong>Status:</strong> {{ props.detection.status }}</p>
        <p><strong>Date:</strong> {{ formatDate(props.detection.created_at) }}</p>
      </div>

      <div v-if="props.detection.items.length" class="items">
        <h4>Detections</h4>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Label</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in props.detection.items" :key="item.id">
              <td>{{ index + 1 }}</td>
              <td>{{ item.label }}</td>
              <td>{{ (item.confidence * 100).toFixed(1) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.result-card {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.result-image img {
  width: 100%;
  max-height: 450px;
  object-fit: contain;
  border-radius: 8px;
  background: #f8fafc;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stat-label {
  font-size: 1rem;
  color: #64748b;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #3b82f6;
}

.meta p {
  margin: 0.25rem 0;
  font-size: 0.875rem;
  color: #475569;
}

.items h4 {
  margin: 1rem 0 0.5rem;
  font-size: 0.9rem;
  color: #334155;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

th,
td {
  text-align: left;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

th {
  color: #64748b;
  font-weight: 600;
}
</style>
