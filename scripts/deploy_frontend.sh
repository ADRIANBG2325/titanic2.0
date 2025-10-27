#!/bin/bash

# Script para preparar el frontend para despliegue

echo "🚀 Preparando frontend para despliegue..."

# Verificar que estamos en el directorio correcto
if [ ! -f "frontend-react/package.json" ]; then
    echo "❌ Error: No se encuentra frontend-react/package.json"
    exit 1
fi

cd frontend-react

# Instalar dependencias
echo "📦 Instalando dependencias..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

# Verificar que existe .env.production
if [ ! -f ".env.production" ]; then
    echo "⚠️  Advertencia: No se encuentra .env.production"
    echo "Creando archivo de ejemplo..."
    echo "VITE_API_URL=https://tu-backend.onrender.com/api" > .env.production
fi

# Build de producción
echo "🏗️  Construyendo para producción..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Error al construir el proyecto"
    exit 1
fi

echo "✅ Frontend listo para despliegue"
echo ""
echo "📝 Próximos pasos:"
echo "1. Actualiza VITE_API_URL en .env.production con tu URL de backend"
echo "2. Sube el código a GitHub"
echo "3. Conecta tu repositorio en Netlify o Vercel"
echo "4. Configura la variable de entorno VITE_API_URL"
echo "5. Despliega!"

cd ..
