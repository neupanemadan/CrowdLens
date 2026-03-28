import { defineStore } from 'pinia'
import { ref } from 'vue'
import { detectionApi } from '@/api'
import type { Detection, DetectionListItem } from '@/types'

export const useDetectionStore = defineStore('detection', () => {
  const currentDetection = ref<Detection | null>(null)
  const detections = ref<DetectionListItem[]>([])
  const isUploading = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function uploadImage(file: File) {
    isUploading.value = true
    error.value = null
    try {
      currentDetection.value = await detectionApi.uploadImage(file)
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } }
      error.value = e.response?.data?.detail || 'Upload failed'
      throw err
    } finally {
      isUploading.value = false
    }
  }

  async function fetchDetections() {
    isLoading.value = true
    error.value = null
    try {
      detections.value = await detectionApi.getAll()
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } }
      error.value = e.response?.data?.detail || 'Failed to load detections'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchDetection(id: number) {
    isLoading.value = true
    error.value = null
    try {
      currentDetection.value = await detectionApi.getById(id)
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } }
      error.value = e.response?.data?.detail || 'Failed to load detection'
    } finally {
      isLoading.value = false
    }
  }

  function clearCurrent() {
    currentDetection.value = null
    error.value = null
  }

  return {
    currentDetection,
    detections,
    isUploading,
    isLoading,
    error,
    uploadImage,
    fetchDetections,
    fetchDetection,
    clearCurrent,
  }
})
