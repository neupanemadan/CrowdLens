<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'file-selected', file: File): void
}>()

const dragActive = ref(false)
const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

function handleDrop(event: DragEvent) {
  dragActive.value = false
  const file = event.dataTransfer?.files[0]
  if (file) selectFile(file)
}

function handleInput(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) selectFile(file)
}

function selectFile(file: File) {
  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)
  emit('file-selected', file)
}

function clearSelection() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  selectedFile.value = null
  previewUrl.value = null
}

defineExpose({ clearSelection })
</script>

<template>
  <div
    class="dropzone"
    :class="{ active: dragActive }"
    @dragover.prevent="dragActive = true"
    @dragleave.prevent="dragActive = false"
    @drop.prevent="handleDrop"
  >
    <div v-if="!previewUrl" class="dropzone-content">
      <p class="dropzone-icon">📷</p>
      <p>Drag & drop an image here</p>
      <p class="dropzone-or">or</p>
      <label class="dropzone-btn">
        Browse Files
        <input hidden type="file" accept="image/*" @change="handleInput" />
      </label>
    </div>
    <div v-else class="preview">
      <img :src="previewUrl" alt="Preview" />
      <p class="filename">{{ selectedFile?.name }}</p>
      <button class="clear-btn" @click="clearSelection">Remove</button>
    </div>
  </div>
</template>

<style scoped>
.dropzone {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition:
    border-color 0.2s,
    background 0.2s;
  cursor: pointer;
}

.dropzone.active {
  border-color: #3b82f6;
  background: #eff6ff;
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
}

.dropzone-icon {
  font-size: 2.5rem;
}

.dropzone-or {
  font-size: 0.75rem;
  color: #94a3b8;
}

.dropzone-btn {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background: #3b82f6;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background 0.2s;
}

.dropzone-btn:hover {
  background: #2563eb;
}

.preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  object-fit: contain;
}

.filename {
  font-size: 0.875rem;
  color: #475569;
}

.clear-btn {
  padding: 0.375rem 1rem;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  color: #64748b;
  cursor: pointer;
  font-size: 0.8rem;
}

.clear-btn:hover {
  border-color: #dc2626;
  color: #dc2626;
}
</style>
