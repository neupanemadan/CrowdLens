<script setup lang="ts">
import type { DetectionListItem } from '@/types'

defineProps<{
  detections: DetectionListItem[]
}>()

const emit = defineEmits<{
  (e: 'select', id: number): void
}>()

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleString()
}
</script>

<template>
  <div class="history-table">
    <table v-if="detections.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>File</th>
          <th>People</th>
          <th>Status</th>
          <th>Date</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="det in detections" :key="det.id">
          <td>{{ det.id }}</td>
          <td>{{ det.original_filename }}</td>
          <td>{{ det.person_count }}</td>
          <td>{{ det.status }}</td>
          <td>{{ formatDate(det.created_at) }}</td>
          <td>
            <button class="view-btn" @click="emit('select', det.id)">View</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty">No detections yet.</p>
  </div>
</template>

<style scoped>
.history-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

th,
td {
  text-align: left;
  padding: 0.625rem 0.75rem;
  border-bottom: 1px solid #e2e8f0;
}

th {
  color: #64748b;
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.view-btn {
  padding: 0.3rem 0.75rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
}

.view-btn:hover {
  background: #2563eb;
}

.empty {
  color: #94a3b8;
  text-align: center;
  padding: 2rem;
}
</style>
