# Titanic Predictor - Frontend React

Frontend moderno construido con React, TypeScript y Vite para el sistema de predicción de supervivencia del Titanic.

## Características

- ⚛️ React 18 con TypeScript
- ⚡ Vite para desarrollo rápido
- 🎨 CSS moderno con variables y animaciones
- 🔒 Validación de formularios en tiempo real
- 📊 Visualización de resultados interactiva
- 🌐 Integración con API Django REST
- 📱 Diseño responsive

## Instalación

\`\`\`bash
cd frontend-react
npm install
\`\`\`

## Configuración

Crea un archivo `.env` basado en `.env.example`:

\`\`\`bash
cp .env.example .env
\`\`\`

Asegúrate de que la URL de la API apunte a tu backend Django:

\`\`\`
VITE_API_URL=http://localhost:8000/api
\`\`\`

## Desarrollo

Inicia el servidor de desarrollo:

\`\`\`bash
npm run dev
\`\`\`

El frontend estará disponible en `http://localhost:5173`

## Construcción para Producción

\`\`\`bash
npm run build
\`\`\`

Los archivos optimizados se generarán en el directorio `dist/`

## Estructura del Proyecto

\`\`\`
frontend-react/
├── src/
│   ├── components/          # Componentes React
│   │   ├── PredictionForm.tsx
│   │   ├── ResultCard.tsx
│   │   └── FunFact.tsx
│   ├── services/            # Servicios de API
│   │   └── api.ts
│   ├── types/               # Definiciones TypeScript
│   │   └── index.ts
│   ├── App.tsx              # Componente principal
│   ├── App.css
│   ├── main.tsx             # Punto de entrada
│   └── index.css            # Estilos globales
├── public/                  # Archivos estáticos
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
\`\`\`

## Uso

1. Asegúrate de que el backend Django esté corriendo en `http://localhost:8000`
2. Inicia el frontend con `npm run dev`
3. Abre `http://localhost:5173` en tu navegador
4. Completa el formulario con los datos del pasajero
5. Haz clic en "Predecir Supervivencia"
6. Visualiza los resultados con probabilidades y factores influyentes

## Validaciones Implementadas

- **Edad**: 0-120 años
- **SibSp**: 0-10 hermanos/cónyuge
- **Parch**: 0-10 padres/hijos
- **Fare**: $0-$600
- **Campos categóricos**: Validación de valores permitidos
- **Validación en tiempo real**: Feedback inmediato al usuario

## Tecnologías

- React 18.3
- TypeScript 5.2
- Vite 5.3
- Axios para peticiones HTTP
- CSS moderno con variables y animaciones
