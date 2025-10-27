"use client"

import { useState, useEffect } from "react"
import { getModelInfo } from "../services/api"
import "./FunFact.css"

export default function FunFact() {
  const [fact, setFact] = useState<string>("Cargando dato curioso...")

  useEffect(() => {
    const loadFact = async () => {
      const info = await getModelInfo()
      if (info?.fun_fact) {
        setFact(info.fun_fact)
      } else {
        setFact("El Titanic era el barco más grande del mundo en 1912.")
      }
    }
    loadFact()
  }, [])

  return (
    <div className="fun-fact">
      <span className="fact-icon">💡</span>
      <p className="fact-text">{fact}</p>
    </div>
  )
}
