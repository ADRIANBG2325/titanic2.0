"use client"

import { useState, useEffect } from "react"
import PredictionForm from "./components/PredictionForm"
import ResultCard from "./components/ResultCard"
import FunFact from "./components/FunFact"
import { checkAPIHealth } from "./services/api"
import type { PredictionResult } from "./types"
import "./App.css"

function App() {
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [apiHealthy, setApiHealthy] = useState<boolean>(true)

  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await checkAPIHealth()
      setApiHealthy(healthy)
    }
    checkHealth()
  }, [])

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1 className="title">
            <span className="icon">🚢</span>
            Predictor de Supervivencia del Titanic
          </h1>
          <p className="subtitle">Descubre si habrías sobrevivido al hundimiento del Titanic usando Machine Learning</p>
          {!apiHealthy && (
            <div className="alert alert-warning">
              ⚠️ Advertencia: No se pudo conectar con el servidor. Asegúrate de que Django esté corriendo en
              http://localhost:8000
            </div>
          )}
        </div>
      </header>

      <main className="main">
        <div className="container">
          <FunFact />

          <div className="content-grid">
            <div className="form-section">
              <PredictionForm onResult={setResult} />
            </div>

            {result && (
              <div className="result-section">
                <ResultCard result={result} />
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <p>Proyecto de Machine Learning - Predicción de Supervivencia del Titanic</p>
          <p>Modelo entrenado con datos históricos del RMS Titanic (1912)</p>
        </div>
      </footer>
    </div>
  )
}

export default App
