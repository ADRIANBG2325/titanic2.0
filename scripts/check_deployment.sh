#!/bin/bash

# Script para verificar que el despliegue está funcionando correctamente

echo "🔍 Verificando despliegue..."
echo ""

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "Uso: ./scripts/check_deployment.sh <URL_BACKEND> [URL_FRONTEND]"
    echo "Ejemplo: ./scripts/check_deployment.sh https://titanic-api.onrender.com https://titanic-app.netlify.app"
    exit 1
fi

BACKEND_URL=$1
FRONTEND_URL=$2

# Verificar backend
echo "📡 Verificando backend: $BACKEND_URL"
echo ""

# Health check
echo "1. Health Check..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/api/health/")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Backend está funcionando"
    echo "   Respuesta: $BODY"
else
    echo "❌ Backend no responde correctamente (HTTP $HTTP_CODE)"
    echo "   Respuesta: $BODY"
fi

echo ""

# Verificar endpoint de predicción
echo "2. Endpoint de predicción..."
PREDICT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BACKEND_URL/api/predict/" \
  -H "Content-Type: application/json" \
  -d '{
    "pclass": 3,
    "sex": "male",
    "age": 22,
    "sibsp": 1,
    "parch": 0,
    "fare": 7.25,
    "embarked": "S"
  }')

HTTP_CODE=$(echo "$PREDICT_RESPONSE" | tail -n1)
BODY=$(echo "$PREDICT_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Endpoint de predicción funciona"
    echo "   Respuesta: $BODY"
else
    echo "❌ Endpoint de predicción falló (HTTP $HTTP_CODE)"
    echo "   Respuesta: $BODY"
fi

echo ""

# Verificar frontend si se proporcionó URL
if [ ! -z "$FRONTEND_URL" ]; then
    echo "🎨 Verificando frontend: $FRONTEND_URL"
    echo ""
    
    FRONTEND_RESPONSE=$(curl -s -w "\n%{http_code}" "$FRONTEND_URL")
    HTTP_CODE=$(echo "$FRONTEND_RESPONSE" | tail -n1)
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Frontend está accesible"
    else
        echo "❌ Frontend no responde correctamente (HTTP $HTTP_CODE)"
    fi
fi

echo ""
echo "🎉 Verificación completada"
