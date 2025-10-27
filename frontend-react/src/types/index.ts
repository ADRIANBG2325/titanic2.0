export interface PassengerData {
  Pclass: number
  Sex: string
  Age: number | null
  SibSp: number
  Parch: number
  Fare: number | null
  Embarked: string
  Name?: string
  Cabin?: string
}

export interface PredictionResult {
  prediccion: string
  probabilidad_sobrevivir: string
  probabilidad_no_sobrevivir: string
  confianza: string
  mensaje_confianza: string
  factores_influyentes: string[]
  dato_curioso: string
  input_procesado: {
    clase: string
    sexo: string
    edad: string
    familia: string
    tarifa: string
    puerto: string
  }
}

export interface APIError {
  error: string
  message?: string
  details?: string[]
}

export interface HealthResponse {
  status: string
  model_loaded: boolean
  metadata_loaded: boolean
  fun_fact: string
}

export interface ModelInfoResponse {
  status: string
  model_info: {
    type: string
    validation_accuracy: string
    features_required: string[]
  }
  valid_inputs: Record<string, string[]>
  input_ranges: Record<string, { min: number; max: number }>
  fun_fact: string
}
