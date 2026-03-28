import apiClient from './client'
import type { Detection, DetectionListItem } from '@/types'

export const detectionApi = {
  async uploadImage(file: File): Promise<Detection> {
    const formData = new FormData()
    formData.append('file', file)

    const { data } = await apiClient.post<Detection>('/detections/image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data
  },

  async getAll(skip = 0, limit = 50): Promise<DetectionListItem[]> {
    const { data } = await apiClient.get<DetectionListItem[]>('/detections', {
      params: { skip, limit },
    })
    return data
  },

  async getById(id: number): Promise<Detection> {
    const { data } = await apiClient.get<Detection>(`/detections/${id}`)
    return data
  },
}
