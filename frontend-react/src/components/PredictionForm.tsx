"use client"

import { useState, type FormEvent, type ChangeEvent } from "react"
import { predictSurvival } from "../services/api"
import type { PassengerData, PredictionResult, APIError } from "../types"
import "./PredictionForm.css"

interface Props {
  onResult: (result: PredictionResult) => void
}

interface FormErrors {
  age?: string
  sibsp?: string
  parch?: string
  fare?: string
}

export default function PredictionForm({ onResult }: Props) {
  const [formData, setFormData] = useState<PassengerData>({
    Pclass: 3,
    Sex: "male",
    Age: null,
    SibSp: 0,
    Parch: 0,
    Fare: null,
    Embarked: "S",
    Name: "",
  })

  const [errors, setErrors] = useState<FormErrors>({})
  const [loading, setLoading] = useState(false)
  const [notification, setNotification] = useState<{ message: string; type: "success" | "error" | "warning" } | null>(
    null,
  )

  const validateField = (name: string, value: number | null, min: number, max: number): string | undefined => {
    if (value === null || value === undefined) return undefined
    if (isNaN(value)) return "Debe ser un número válido"
    if (value < min || value > max) return `Debe estar entre ${min} y ${max}`
    return undefined
  }

  const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target

    let processedValue: string | number | null = value

    if (name === "Pclass" || name === "SibSp" || name === "Parch") {
      processedValue = value ? Number.parseInt(value) : 0
    } else if (name === "Age" || name === "Fare") {
      processedValue = value ? Number.parseFloat(value) : null
    }

    setFormData((prev) => ({ ...prev, [name]: processedValue }))

    // Validación en tiempo real
    if (name === "Age") {
      const error = validateField(name, processedValue as number | null, 0, 120)
      setErrors((prev) => ({ ...prev, age: error }))
    } else if (name === "SibSp") {
      const error = validateField(name, processedValue as number, 0, 10)
      setErrors((prev) => ({ ...prev, sibsp: error }))
    } else if (name === "Parch") {
      const error = validateField(name, processedValue as number, 0, 10)
      setErrors((prev) => ({ ...prev, parch: error }))
    } else if (name === "Fare") {
      const error = validateField(name, processedValue as number | null, 0, 600)
      setErrors((prev) => ({ ...prev, fare: error }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {}

    if (formData.Age !== null) {
      newErrors.age = validateField("Age", formData.Age, 0, 120)
    }
    newErrors.sibsp = validateField("SibSp", formData.SibSp, 0, 10)
    newErrors.parch = validateField("Parch", formData.Parch, 0, 10)
    if (formData.Fare !== null) {
      newErrors.fare = validateField("Fare", formData.Fare, 0, 600)
    }

    setErrors(newErrors)
    return !Object.values(newErrors).some((error) => error !== undefined)
  }

  const showNotification = (message: string, type: "success" | "error" | "warning") => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 5000)
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()

    if (!validateForm()) {
      showNotification("Por favor corrige los errores en el formulario", "error")
      return
    }

    setLoading(true)

    try {
      const result = await predictSurvival(formData)
      onResult(result)
      showNotification("Predicción realizada exitosamente", "success")

      // Scroll suave al resultado
      setTimeout(() => {
        document.querySelector(".result-section")?.scrollIntoView({ behavior: "smooth", block: "nearest" })
      }, 100)
    } catch (error) {
      const apiError = error as APIError
      let errorMessage = "Error al realizar la predicción"

      if (apiError.details && Array.isArray(apiError.details)) {
        errorMessage = apiError.details.join("\n")
      } else if (apiError.message) {
        errorMessage = apiError.message
      } else if (apiError.error) {
        errorMessage = apiError.error
      }

      showNotification(errorMessage, "error")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="form-container">
      {notification && <div className={`notification notification-${notification.type}`}>{notification.message}</div>}

      <form onSubmit={handleSubmit} className="prediction-form">
        <h2 className="form-title">Ingresa los datos del pasajero</h2>

        <div className="form-grid">
          <div className="form-group">
            <label htmlFor="pclass">Clase del Boleto</label>
            <select id="pclass" name="Pclass" value={formData.Pclass} onChange={handleInputChange} required>
              <option value={1}>1ª Clase (Primera)</option>
              <option value={2}>2ª Clase (Segunda)</option>
              <option value={3}>3ª Clase (Tercera)</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="sex">Sexo</label>
            <select id="sex" name="Sex" value={formData.Sex} onChange={handleInputChange} required>
              <option value="male">Hombre</option>
              <option value="female">Mujer</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="age">Edad (años)</label>
            <input
              type="number"
              id="age"
              name="Age"
              value={formData.Age ?? ""}
              onChange={handleInputChange}
              placeholder="Ej: 25"
              min="0"
              max="120"
              step="0.1"
              className={errors.age ? "error" : ""}
            />
            {errors.age && <span className="error-message">{errors.age}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="sibsp">Hermanos/Cónyuge a bordo</label>
            <input
              type="number"
              id="sibsp"
              name="SibSp"
              value={formData.SibSp}
              onChange={handleInputChange}
              min="0"
              max="10"
              required
              className={errors.sibsp ? "error" : ""}
            />
            {errors.sibsp && <span className="error-message">{errors.sibsp}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="parch">Padres/Hijos a bordo</label>
            <input
              type="number"
              id="parch"
              name="Parch"
              value={formData.Parch}
              onChange={handleInputChange}
              min="0"
              max="10"
              required
              className={errors.parch ? "error" : ""}
            />
            {errors.parch && <span className="error-message">{errors.parch}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="fare">Tarifa Pagada ($)</label>
            <input
              type="number"
              id="fare"
              name="Fare"
              value={formData.Fare ?? ""}
              onChange={handleInputChange}
              placeholder="Ej: 32.50"
              min="0"
              max="600"
              step="0.01"
              className={errors.fare ? "error" : ""}
            />
            {errors.fare && <span className="error-message">{errors.fare}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="embarked">Puerto de Embarque</label>
            <select id="embarked" name="Embarked" value={formData.Embarked} onChange={handleInputChange} required>
              <option value="S">Southampton</option>
              <option value="C">Cherbourg</option>
              <option value="Q">Queenstown</option>
            </select>
          </div>

          <div className="form-group form-group-full">
            <label htmlFor="name">Nombre (Opcional)</label>
            <input
              type="text"
              id="name"
              name="Name"
              value={formData.Name}
              onChange={handleInputChange}
              placeholder="Ej: Smith, Mr. John"
            />
          </div>
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? (
            <>
              <span className="btn-icon">⏳</span>
              Procesando...
            </>
          ) : (
            <>
              <span className="btn-icon">🔮</span>
              Predecir Supervivencia
            </>
          )}
        </button>
      </form>
    </div>
  )
}
