#!/bin/bash

# Script para preparar el backend para despliegue

echo "🚀 Preparando backend para despliegue..."

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: No se encuentra manage.py. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# Crear directorio de modelos si no existe
mkdir -p models

# Entrenar el modelo
echo "🤖 Entrenando modelo..."
python scripts/01_data_analysis_and_training.py

if [ $? -ne 0 ]; then
    echo "❌ Error al entrenar el modelo"
    exit 1
fi

# Verificar que el modelo se creó
if [ ! -f "models/titanic_model.pkl" ]; then
    echo "❌ Error: El modelo no se generó correctamente"
    exit 1
fi

echo "✅ Modelo entrenado exitosamente"

# Recolectar archivos estáticos
echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Ejecutar migraciones
echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

echo "✅ Backend listo para despliegue"
echo ""
echo "📝 Próximos pasos:"
echo "1. Sube el código a GitHub"
echo "2. Conecta tu repositorio en Render o Railway"
echo "3. Configura las variables de entorno"
echo "4. Despliega!"
