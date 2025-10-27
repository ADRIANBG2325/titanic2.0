"""
Vista de predicción con validaciones robustas y manejo de errores completo
"""

import joblib
import pandas as pd
import numpy as np
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render

# ============================================================================
# CARGA DEL MODELO Y METADATA AL INICIO
# ============================================================================
pipeline = None
metadata = None

try:
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'models', 'titanic_pipeline.pkl'),
        './models/titanic_pipeline.pkl',
        './titanic_pipeline.pkl',
        os.path.join(settings.BASE_DIR, 'predictor', 'titanic_pipeline.pkl'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            pipeline = joblib.load(path)
            print(f"✅ Pipeline cargado exitosamente desde: {path}")
            break
    
    if pipeline is None:
        print("❌ ERROR: No se pudo encontrar titanic_pipeline.pkl")
        print("   Ubicaciones buscadas:")
        for path in possible_paths:
            print(f"   - {path}")
    
    metadata_paths = [
        os.path.join(settings.BASE_DIR, 'models', 'model_metadata.json'),
        './models/model_metadata.json',
        './model_metadata.json',
        os.path.join(settings.BASE_DIR, 'predictor', 'model_metadata.json'),
    ]
    
    for path in metadata_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                metadata = json.load(f)
            print(f"✅ Metadata cargada exitosamente desde: {path}")
            break
            
except Exception as e:
    print(f"❌ ERROR al cargar el pipeline o metadata: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# DATOS CURIOSOS SOBRE EL TITANIC
# ============================================================================
TITANIC_FACTS = [
    "El Titanic tenía 4 chimeneas, pero solo 3 funcionaban. La cuarta era decorativa.",
    "La orquesta del Titanic tocó hasta el final. Ninguno de sus 8 miembros sobrevivió.",
    "El boleto más caro costó £870 (equivalente a ~$100,000 hoy en día).",
    "Solo el 20% de los hombres sobrevivieron, comparado con el 74% de las mujeres.",
    "Los pasajeros de 1ra clase tenían 3 veces más probabilidad de sobrevivir que los de 3ra.",
    "El agua estaba a -2°C. La mayoría murió de hipotermia en 15-30 minutos.",
    "El Titanic tenía botes salvavidas para solo 1,178 personas de 2,224 a bordo.",
    "Los niños de 1ra y 2da clase tuvieron 100% de supervivencia, pero solo 34% en 3ra clase."
]

# ============================================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================================

def validate_numeric_field(value, field_name, min_val=None, max_val=None, allow_null=False):
    """Valida campos numéricos con rangos opcionales"""
    if value is None or value == '':
        if allow_null:
            return None, None
        return None, f"{field_name} es requerido"
    
    try:
        num_value = float(value)
        
        if np.isnan(num_value) or np.isinf(num_value):
            return None, f"{field_name} contiene un valor inválido"
        
        if min_val is not None and num_value < min_val:
            return None, f"{field_name} debe ser mayor o igual a {min_val}"
        
        if max_val is not None and num_value > max_val:
            return None, f"{field_name} debe ser menor o igual a {max_val}"
        
        return num_value, None
    except (ValueError, TypeError):
        return None, f"{field_name} debe ser un número válido"

def validate_categorical_field(value, field_name, valid_values):
    """Valida campos categóricos contra valores permitidos"""
    if value is None or value == '':
        return None, f"{field_name} es requerido"
    
    # Convertir a string y limpiar
    str_value = str(value).strip()
    
    if str_value not in valid_values:
        return None, f"{field_name} debe ser uno de: {', '.join(map(str, valid_values))}"
    
    return str_value, None

def extract_title_from_name(name):
    """Extrae título del nombre con manejo de errores"""
    try:
        if not name or pd.isna(name):
            return 'Mr'  # Default
        title = name.split(',')[1].split('.')[0].strip()
        if title in ['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 
                     'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona']:
            return 'Rare'
        elif title in ['Mlle', 'Ms']:
            return 'Miss'
        elif title == 'Mme':
            return 'Mrs'
        return title
    except:
        return 'Mr'

def extract_deck_from_cabin(cabin):
    """Extrae deck de la cabina"""
    try:
        if not cabin or pd.isna(cabin):
            return 'U'
        return cabin[0].upper()
    except:
        return 'U'

def create_age_group_from_age(age):
    """Crea grupo de edad"""
    try:
        if pd.isna(age):
            return 'Adult'  # Default
        if age < 12:
            return 'Child'
        elif age < 18:
            return 'Teen'
        elif age < 35:
            return 'Young_Adult'
        elif age < 60:
            return 'Adult'
        else:
            return 'Senior'
    except:
        return 'Adult'

# ============================================================================
# VISTA DE PREDICCIÓN
# ============================================================================

class PredictView(APIView):
    """
    Vista para realizar predicciones de supervivencia del Titanic
    con validaciones exhaustivas y manejo de errores robusto
    """
    
    def get(self, request, *args, **kwargs):
        """Endpoint GET para obtener información del modelo"""
        if not pipeline or not metadata:
            return Response({
                "error": "Modelo no disponible",
                "message": "El modelo no se ha cargado correctamente. Contacte al administrador."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response({
            "status": "operational",
            "model_info": {
                "type": metadata.get('model_type', 'Unknown'),
                "validation_accuracy": f"{metadata.get('validation_score', 0) * 100:.2f}%",
                "features_required": metadata.get('features', [])
            },
            "valid_inputs": metadata.get('valid_values', {}),
            "input_ranges": metadata.get('feature_ranges', {}),
            "fun_fact": np.random.choice(TITANIC_FACTS)
        })
    
    def post(self, request, *args, **kwargs):
        """Endpoint POST para realizar predicciones"""
        
        # Verificar que el modelo esté cargado
        if not pipeline:
            return Response({
                "error": "Modelo no disponible",
                "message": "El modelo no se ha cargado correctamente."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        data = request.data
        errors = []
        
        # ====================================================================
        # VALIDACIÓN DE CAMPOS REQUERIDOS
        # ====================================================================
        
        # Validar Pclass (1, 2, 3)
        pclass, error = validate_categorical_field(
            data.get('Pclass'), 'Pclass', ['1', '2', '3', 1, 2, 3]
        )
        if error:
            errors.append(error)
        else:
            pclass = int(pclass)
        
        # Validar Sex (male, female)
        sex, error = validate_categorical_field(
            data.get('Sex'), 'Sex', ['male', 'female']
        )
        if error:
            errors.append(error)
        
        # Validar Age (0-100)
        age, error = validate_numeric_field(
            data.get('Age'), 'Age', min_val=0, max_val=120, allow_null=True
        )
        if error:
            errors.append(error)
        elif age is None:
            age = 30  # Valor por defecto si no se proporciona
        
        # Validar SibSp (0-10)
        sibsp, error = validate_numeric_field(
            data.get('SibSp'), 'SibSp', min_val=0, max_val=10
        )
        if error:
            errors.append(error)
        else:
            sibsp = int(sibsp)
        
        # Validar Parch (0-10)
        parch, error = validate_numeric_field(
            data.get('Parch'), 'Parch', min_val=0, max_val=10
        )
        if error:
            errors.append(error)
        else:
            parch = int(parch)
        
        # Validar Fare (0-600)
        fare, error = validate_numeric_field(
            data.get('Fare'), 'Fare', min_val=0, max_val=600, allow_null=True
        )
        if error:
            errors.append(error)
        elif fare is None:
            fare = 32.0  # Valor mediano por defecto
        
        # Validar Embarked (C, Q, S)
        embarked, error = validate_categorical_field(
            data.get('Embarked'), 'Embarked', ['C', 'Q', 'S']
        )
        if error:
            errors.append(error)
        
        # Si hay errores de validación, retornar
        if errors:
            return Response({
                "error": "Errores de validación",
                "details": errors,
                "message": "Por favor corrija los campos indicados"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # ====================================================================
        # INGENIERÍA DE CARACTERÍSTICAS
        # ====================================================================
        
        try:
            # Campos opcionales
            name = data.get('Name', '')
            cabin = data.get('Cabin', '')
            
            # Crear características derivadas
            title = extract_title_from_name(name)
            family_size = sibsp + parch + 1
            is_alone = 1 if family_size == 1 else 0
            deck = extract_deck_from_cabin(cabin)
            age_group = create_age_group_from_age(age)
            fare_log = np.log1p(fare)
            
            # Construir DataFrame con TODAS las características que espera el modelo
            input_data = {
                'Pclass': pclass,
                'Sex': sex,
                'Age': age,
                'SibSp': sibsp,
                'Parch': parch,
                'Fare_Log': fare_log,
                'Embarked': embarked,
                'Title': title,
                'FamilySize': family_size,
                'IsAlone': is_alone,
                'Deck': deck,
                'Age_Group': age_group
            }
            
            input_df = pd.DataFrame([input_data])
            
            # Validar que no hay valores NaN o Inf
            if input_df.isnull().any().any():
                return Response({
                    "error": "Datos incompletos",
                    "message": "Algunos campos contienen valores inválidos"
                }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "error": "Error en procesamiento de características",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # ====================================================================
        # REALIZAR PREDICCIÓN
        # ====================================================================
        
        try:
            # Predicción
            prediction = pipeline.predict(input_df)[0]
            prediction_proba = pipeline.predict_proba(input_df)[0]
            
            # Probabilidades
            prob_no_survive = prediction_proba[0] * 100
            prob_survive = prediction_proba[1] * 100
            
            # Resultado
            result = "Sobrevive" if prediction == 1 else "No Sobrevive"
            confidence = max(prob_no_survive, prob_survive)
            
            # Mensaje contextual basado en la confianza
            if confidence > 80:
                confidence_msg = "Alta confianza en la predicción"
            elif confidence > 60:
                confidence_msg = "Confianza moderada en la predicción"
            else:
                confidence_msg = "Baja confianza - resultado incierto"
            
            # Factores que influyeron (análisis simple)
            factors = []
            if sex == 'female':
                factors.append("Ser mujer aumentaba significativamente las probabilidades de supervivencia")
            if pclass == 1:
                factors.append("Viajar en 1ra clase triplicaba las probabilidades de supervivencia")
            elif pclass == 3:
                factors.append("Viajar en 3ra clase reducía drásticamente las probabilidades")
            if age < 12:
                factors.append("Los niños tenían prioridad en los botes salvavidas")
            if family_size > 4:
                factors.append("Familias grandes tenían más dificultad para evacuar juntas")
            
            return Response({
                "prediccion": result,
                "probabilidad_sobrevivir": f"{prob_survive:.2f}%",
                "probabilidad_no_sobrevivir": f"{prob_no_survive:.2f}%",
                "confianza": f"{confidence:.2f}%",
                "mensaje_confianza": confidence_msg,
                "factores_influyentes": factors,
                "dato_curioso": np.random.choice(TITANIC_FACTS),
                "input_procesado": {
                    "clase": f"{pclass}ª clase",
                    "sexo": "Hombre" if sex == 'male' else "Mujer",
                    "edad": f"{age:.0f} años",
                    "familia": f"{family_size} miembros",
                    "tarifa": f"${fare:.2f}",
                    "puerto": {"C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"}.get(embarked, embarked)
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Error en la predicción",
                "message": f"Ocurrió un error al procesar la predicción: {str(e)}",
                "details": "Por favor verifique que todos los datos sean correctos"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HealthCheckView(APIView):
    """Vista para verificar el estado del servicio"""
    
    def get(self, request, *args, **kwargs):
        model_loaded = pipeline is not None
        metadata_loaded = metadata is not None
        
        return Response({
            "status": "healthy" if (model_loaded and metadata_loaded) else "unhealthy",
            "model_loaded": model_loaded,
            "metadata_loaded": metadata_loaded,
            "fun_fact": np.random.choice(TITANIC_FACTS)
        })

def index_view(request):
    """Vista para servir el frontend HTML"""
    import os
    frontend_path = os.path.join(settings.BASE_DIR, 'frontend', 'index.html')
    
    try:
        with open(frontend_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        from django.http import HttpResponse
        return HttpResponse(html_content)
    except FileNotFoundError:
        from django.http import HttpResponse
        return HttpResponse(
            "<h1>Error: Frontend no encontrado</h1>"
            "<p>Asegúrate de que el archivo frontend/index.html existe</p>",
            status=404
        )
