<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDetectionStore } from '@/stores'
import ImageUploader from '@/components/detection/ImageUploader.vue'
import AppLoader from '@/components/common/AppLoader.vue'
import AppError from '@/components/common/AppError.vue'

const store = useDetectionStore()
const router = useRouter()
const selectedFile = ref<File | null>(null)

function onFileSelected(file: File) {
  selectedFile.value = file
  store.clearCurrent()
}

async function handleUpload() {
  if (!selectedFile.value) return
  try {
    await store.uploadImage(selectedFile.value)
    router.push({ name: 'result' })
  } catch {
    // error is set in store
  }
}
</script>

<template>
  <div class="upload-view">
    <h1>Upload Image</h1>
    <p class="subtitle">Upload an image to detect and count people.</p>

    <ImageUploader @file-selected="onFileSelected" />

    <AppError v-if="store.error" :message="store.error" />

    <AppLoader v-if="store.isUploading" text="Detecting people..." />

    <button v-if="selectedFile && !store.isUploading" class="detect-btn" @click="handleUpload">
      Detect People
    </button>
  </div>
</template>

<style scoped>
.upload-view {
  max-width: 600px;
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

.subtitle {
  color: #64748b;
  font-size: 0.9rem;
  margin: 0;
}

.detect-btn {
  padding: 0.75rem 2rem;
  background: #3b82f6;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  align-self: center;
}

.detect-btn:hover {
  background: #2563eb;
}
</style>
