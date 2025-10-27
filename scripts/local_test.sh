#!/bin/bash

# Script para probar la aplicación localmente antes de desplegar

echo "🧪 Probando aplicación localmente..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto"
    exit 1
fi

# Verificar entorno virtual
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Advertencia: No estás en un entorno virtual"
    echo "   Recomendado: source venv/bin/activate"
    read -p "¿Continuar de todos modos? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Instalar dependencias del backend
echo "📦 Instalando dependencias del backend..."
pip install -r requirements.txt -q

# Ejecutar migraciones
echo "🗄️  Ejecutando migraciones..."
python manage.py migrate

# Entrenar modelo
echo "🤖 Entrenando modelo..."
python scripts/01_data_analysis_and_training.py

if [ ! -f "models/titanic_model.pkl" ]; then
    echo "❌ Error: El modelo no se generó correctamente"
    exit 1
fi

echo "✅ Modelo entrenado exitosamente"
echo ""

# Probar el backend
echo "🧪 Probando backend..."
python manage.py runserver &
DJANGO_PID=$!

# Esperar a que Django inicie
sleep 3

# Health check
echo "1. Health check..."
HEALTH=$(curl -s http://localhost:8000/api/health/)
echo "   Respuesta: $HEALTH"

# Test de predicción
echo "2. Test de predicción..."
PREDICTION=$(curl -s -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "pclass": 1,
    "sex": "female",
    "age": 25,
    "sibsp": 0,
    "parch": 0,
    "fare": 100,
    "embarked": "C"
  }')
echo "   Respuesta: $PREDICTION"

# Detener Django
kill $DJANGO_PID

echo ""
echo "✅ Tests del backend completados"
echo ""

# Probar el frontend
echo "🎨 Probando frontend..."
cd frontend-react

if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias del frontend..."
    npm install
fi

echo "🏗️  Construyendo frontend..."
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Build del frontend exitoso"
else
    echo "❌ Error en el build del frontend"
    exit 1
fi

cd ..

echo ""
echo "🎉 Todas las pruebas pasaron exitosamente"
echo ""
echo "📝 Próximos pasos:"
echo "1. Inicia el backend: python manage.py runserver"
echo "2. En otra terminal, inicia el frontend: cd frontend-react && npm run dev"
echo "3. Abre http://localhost:5173 en tu navegador"
echo "4. Si todo funciona, estás listo para desplegar"
