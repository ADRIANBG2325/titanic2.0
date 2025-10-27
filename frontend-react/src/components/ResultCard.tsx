import type { PredictionResult } from "../types"
import "./ResultCard.css"

interface Props {
  result: PredictionResult
}

export default function ResultCard({ result }: Props) {
  const survived = result.prediccion === "Sobrevive"
  const probability = Number.parseFloat(result.probabilidad_sobrevivir)

  return (
    <div className={`result-card ${survived ? "success" : "danger"}`}>
      <div className="result-header">
        <span className="result-icon">{survived ? "✅" : "❌"}</span>
        <h2 className="result-title">{result.prediccion}</h2>
      </div>

      <div className="probability-bar">
        <div className="probability-fill" style={{ width: `${probability}%` }} />
      </div>
      <p className="probability-text">Probabilidad de supervivencia: {result.probabilidad_sobrevivir}</p>

      <div className="confidence-badge">
        <span className="confidence-text">{result.mensaje_confianza}</span>
      </div>

      {result.factores_influyentes && result.factores_influyentes.length > 0 && (
        <div className="factors-section">
          <h3>Factores Influyentes:</h3>
          <ul className="factors-list">
            {result.factores_influyentes.map((factor, index) => (
              <li key={index}>{factor}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="input-summary">
        <h3>📋 Resumen de tu perfil:</h3>
        <div className="summary-grid">
          <div className="summary-item">
            <strong>Clase:</strong> {result.input_procesado.clase}
          </div>
          <div className="summary-item">
            <strong>Sexo:</strong> {result.input_procesado.sexo}
          </div>
          <div className="summary-item">
            <strong>Edad:</strong> {result.input_procesado.edad}
          </div>
          <div className="summary-item">
            <strong>Familia:</strong> {result.input_procesado.familia}
          </div>
          <div className="summary-item">
            <strong>Tarifa:</strong> {result.input_procesado.tarifa}
          </div>
          <div className="summary-item">
            <strong>Puerto:</strong> {result.input_procesado.puerto}
          </div>
        </div>
      </div>

      {result.dato_curioso && (
        <div className="result-fact">
          <strong>💡 Dato Curioso:</strong>
          <p>{result.dato_curioso}</p>
        </div>
      )}
    </div>
  )
}
