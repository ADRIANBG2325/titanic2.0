import axios from "axios"
import type { PassengerData, PredictionResult, HealthResponse, ModelInfoResponse } from "../types"

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api"

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
})

export const checkAPIHealth = async (): Promise<boolean> => {
  try {
    const response = await api.get<HealthResponse>("/health/")
    console.log("✅ API Health Check:", response.data)
    return response.data.status === "healthy"
  } catch (error) {
    console.error("❌ API Health Check Failed:", error)
    return false
  }
}

export const getModelInfo = async (): Promise<ModelInfoResponse | null> => {
  try {
    const response = await api.get<ModelInfoResponse>("/predict/")
    console.log("📊 Model Info:", response.data)
    return response.data
  } catch (error) {
    console.error("❌ Error fetching model info:", error)
    return null
  }
}

export const predictSurvival = async (data: PassengerData): Promise<PredictionResult> => {
  try {
    console.log("📤 Sending prediction request:", data)
    const response = await api.post<PredictionResult>("/predict/", data)
    console.log("✅ Prediction received:", response.data)
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      console.error("❌ Prediction error:", error.response.data)
      throw error.response.data
    }
    throw new Error("Error de conexión con el servidor")
  }
}
