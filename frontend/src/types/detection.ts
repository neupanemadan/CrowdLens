export interface DetectionItem {
  id: number
  label: string
  confidence: number
  x_min: number
  y_min: number
  x_max: number
  y_max: number
}

export interface Detection {
  id: number
  original_filename: string
  annotated_image_path: string
  person_count: number
  status: string
  created_at: string
  items: DetectionItem[]
}

export interface DetectionListItem {
  id: number
  original_filename: string
  person_count: number
  status: string
  created_at: string
}

export interface HealthResponse {
  status: string
  app_name: string
}
