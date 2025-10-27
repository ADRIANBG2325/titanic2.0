"""
Script completo para análisis, entrenamiento y guardado del modelo Titanic
Incluye validaciones, manejo de errores y datos curiosos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
import joblib
import json
import warnings
import os
warnings.filterwarnings('ignore')

print("=" * 80)
print("🚢 PROYECTO TITANIC - ANÁLISIS Y ENTRENAMIENTO DEL MODELO")
print("=" * 80)

# ============================================================================
# DATOS CURIOSOS SOBRE EL TITANIC 📊
# ============================================================================
print("\n📚 DATOS CURIOSOS SOBRE EL TITANIC:")
print("-" * 80)
curiosidades = [
    "🎫 El precio del boleto más caro fue £512 (equivalente a ~$61,000 hoy)",
    "👨‍👩‍👧‍👦 Solo el 30% de los pasajeros de 3ra clase sobrevivieron",
    "👔 Los títulos 'Mr' tenían solo 15% de supervivencia vs 'Mrs' con 79%",
    "🚪 La clase del pasajero era el predictor más fuerte de supervivencia",
    "👶 Los niños menores de 10 años tenían mayor probabilidad de sobrevivir",
    "🎻 La banda del Titanic siguió tocando mientras el barco se hundía",
    "❄️ El agua estaba a -2°C, causando hipotermia en minutos",
    "🛟 Solo había botes salvavidas para 1,178 personas de 2,224 a bordo"
]
for dato in curiosidades:
    print(f"  {dato}")
print("-" * 80)

# ============================================================================
# CARGA Y VALIDACIÓN DE DATOS
# ============================================================================
print("\n📂 CARGANDO DATOS...")
try:
    # Intentar cargar desde Kaggle o archivo local
    df = pd.read_csv('train.csv')
    print(f"✅ Datos cargados exitosamente: {df.shape[0]} filas, {df.shape[1]} columnas")
except FileNotFoundError:
    print("❌ ERROR: No se encontró 'train.csv'")
    print("   Descarga los datos de: https://www.kaggle.com/c/titanic/data")
    exit(1)
except Exception as e:
    print(f"❌ ERROR al cargar datos: {str(e)}")
    exit(1)

# Validar columnas requeridas
columnas_requeridas = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 
                       'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
columnas_faltantes = set(columnas_requeridas) - set(df.columns)
if columnas_faltantes:
    print(f"❌ ERROR: Faltan columnas requeridas: {columnas_faltantes}")
    exit(1)

print("\n📊 INFORMACIÓN GENERAL DEL DATASET:")
print(df.info())
print("\n📈 ESTADÍSTICAS DESCRIPTIVAS:")
print(df.describe())

# ============================================================================
# ANÁLISIS EXPLORATORIO CON INSIGHTS
# ============================================================================
print("\n🔍 ANÁLISIS EXPLORATORIO DE DATOS:")
print("-" * 80)

# Tasa de supervivencia general
tasa_supervivencia = df['Survived'].mean() * 100
print(f"📊 Tasa de supervivencia general: {tasa_supervivencia:.2f}%")

# Supervivencia por clase
print("\n🎫 Supervivencia por Clase:")
supervivencia_clase = df.groupby('Pclass')['Survived'].agg(['mean', 'count'])
supervivencia_clase['mean'] = supervivencia_clase['mean'] * 100
print(supervivencia_clase)

# Supervivencia por sexo
print("\n👥 Supervivencia por Sexo:")
supervivencia_sexo = df.groupby('Sex')['Survived'].agg(['mean', 'count'])
supervivencia_sexo['mean'] = supervivencia_sexo['mean'] * 100
print(supervivencia_sexo)

# Valores nulos
print("\n❓ Valores Nulos por Columna:")
nulos = df.isnull().sum()
print(nulos[nulos > 0])

# ============================================================================
# INGENIERÍA DE CARACTERÍSTICAS AVANZADA
# ============================================================================
print("\n🔧 INGENIERÍA DE CARACTERÍSTICAS...")

def extract_title(name):
    """Extrae el título del nombre con manejo de errores"""
    try:
        if pd.isna(name):
            return 'Unknown'
        title = name.split(',')[1].split('.')[0].strip()
        # Agrupar títulos raros
        if title in ['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 
                     'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona']:
            return 'Rare'
        elif title in ['Mlle', 'Ms']:
            return 'Miss'
        elif title == 'Mme':
            return 'Mrs'
        return title
    except:
        return 'Unknown'

def extract_deck(cabin):
    """Extrae el deck de la cabina con validación"""
    try:
        if pd.isna(cabin):
            return 'U'  # Unknown
        return cabin[0]
    except:
        return 'U'

def create_age_group(age):
    """Crea grupos de edad con manejo de nulos"""
    try:
        if pd.isna(age):
            return 'Unknown'
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
        return 'Unknown'

# Aplicar transformaciones con manejo de errores
try:
    df['Title'] = df['Name'].apply(extract_title)
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
    df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
    df['Deck'] = df['Cabin'].apply(extract_deck)
    df['Age_Group'] = df['Age'].apply(create_age_group)
    
    # Transformación logarítmica de Fare (evitar log(0))
    df['Fare_Log'] = np.log1p(df['Fare'].fillna(0))
    
    print("✅ Características creadas exitosamente")
    print(f"   - Title: {df['Title'].nunique()} categorías")
    print(f"   - FamilySize: rango {df['FamilySize'].min()}-{df['FamilySize'].max()}")
    print(f"   - Deck: {df['Deck'].nunique()} decks identificados")
    print(f"   - Age_Group: {df['Age_Group'].nunique()} grupos")
except Exception as e:
    print(f"❌ ERROR en ingeniería de características: {str(e)}")
    exit(1)

# ============================================================================
# IMPUTACIÓN INTELIGENTE DE VALORES NULOS
# ============================================================================
print("\n🔄 IMPUTANDO VALORES NULOS...")

try:
    # Imputar Age por Pclass y Title (más preciso)
    for pclass in df['Pclass'].unique():
        for title in df['Title'].unique():
            mask = (df['Pclass'] == pclass) & (df['Title'] == title) & (df['Age'].isnull())
            median_age = df[(df['Pclass'] == pclass) & (df['Title'] == title)]['Age'].median()
            if pd.notna(median_age):
                df.loc[mask, 'Age'] = median_age
    
    # Imputar Age restante con mediana general
    df['Age'].fillna(df['Age'].median(), inplace=True)
    
    # Imputar Embarked con moda
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    
    # Imputar Fare con mediana
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    
    print("✅ Imputación completada")
    print(f"   Valores nulos restantes: {df.isnull().sum().sum()}")
except Exception as e:
    print(f"❌ ERROR en imputación: {str(e)}")
    exit(1)

# ============================================================================
# PREPARACIÓN DE DATOS PARA ENTRENAMIENTO
# ============================================================================
print("\n🎯 PREPARANDO DATOS PARA ENTRENAMIENTO...")

# Seleccionar características
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare_Log', 
            'Embarked', 'Title', 'FamilySize', 'IsAlone', 'Deck', 'Age_Group']

# Validar que todas las features existen
features_faltantes = set(features) - set(df.columns)
if features_faltantes:
    print(f"❌ ERROR: Faltan features: {features_faltantes}")
    exit(1)

X = df[features].copy()
y = df['Survived'].copy()

# Validar que no hay valores infinitos
if np.isinf(X.select_dtypes(include=[np.number])).any().any():
    print("⚠️  Advertencia: Se encontraron valores infinitos, reemplazando...")
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())

# División de datos con estratificación
try:
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✅ Datos divididos:")
    print(f"   Entrenamiento: {X_train.shape[0]} muestras")
    print(f"   Validación: {X_val.shape[0]} muestras")
    print(f"   Distribución de clases en entrenamiento: {y_train.value_counts().to_dict()}")
except Exception as e:
    print(f"❌ ERROR al dividir datos: {str(e)}")
    exit(1)

# ============================================================================
# CONSTRUCCIÓN DEL PIPELINE DE PREPROCESAMIENTO
# ============================================================================
print("\n🔨 CONSTRUYENDO PIPELINE DE PREPROCESAMIENTO...")

# Identificar columnas numéricas y categóricas
numeric_features = ['Age', 'SibSp', 'Parch', 'Fare_Log', 'FamilySize', 'IsAlone']
categorical_features = ['Pclass', 'Sex', 'Embarked', 'Title', 'Deck', 'Age_Group']

# Pipeline para características numéricas
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para características categóricas
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combinar transformadores
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

print("✅ Pipeline de preprocesamiento creado")

# ============================================================================
# ENTRENAMIENTO Y OPTIMIZACIÓN DEL MODELO
# ============================================================================
print("\n🤖 ENTRENANDO Y OPTIMIZANDO MODELO...")

# Crear pipeline completo
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [5, 8, 10, 12],  # Valores más bajos para evitar árboles muy profundos
    'classifier__min_samples_split': [10, 15, 20],  # Valores más altos para requerir más muestras antes de dividir
    'classifier__min_samples_leaf': [3, 5, 10],  # Valores más altos para hojas más grandes
    'classifier__max_features': ['sqrt', 'log2'],  # Limitar features consideradas en cada split
    'classifier__min_impurity_decrease': [0.0, 0.001, 0.01]  # Requerir mejora mínima para hacer split
}

print("🔍 Realizando búsqueda de hiperparámetros con regularización anti-overfitting...")
print("   Parámetros restrictivos aplicados:")
print("   - max_depth: [5, 8, 10, 12] (más bajo = menos complejo)")
print("   - min_samples_split: [10, 15, 20] (más alto = más conservador)")
print("   - min_samples_leaf: [3, 5, 10] (más alto = hojas más generales)")

try:
    # Grid Search con validación cruzada
    grid_search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=5, 
        scoring='accuracy',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    print("\n✅ OPTIMIZACIÓN COMPLETADA")
    print(f"   Mejores parámetros: {grid_search.best_params_}")
    print(f"   Mejor score CV: {grid_search.best_score_:.4f}")
    
    # Evaluar en conjunto de validación
    val_score = grid_search.score(X_val, y_val)
    train_score = grid_search.score(X_train, y_train)
    
    print(f"\n📊 MÉTRICAS FINALES:")
    print(f"   Accuracy en entrenamiento: {train_score:.4f}")
    print(f"   Accuracy en validación: {val_score:.4f}")
    print(f"   Diferencia (overfitting check): {abs(train_score - val_score):.4f}")
    
    overfitting_gap = abs(train_score - val_score)
    if overfitting_gap > 0.1:
        print(f"   ⚠️  Advertencia: Overfitting detectado (gap: {overfitting_gap:.4f})")
        print("   💡 Sugerencia: El modelo podría beneficiarse de más regularización")
    elif overfitting_gap > 0.05:
        print(f"   ⚠️  Overfitting leve detectado (gap: {overfitting_gap:.4f})")
        print("   ✅ Dentro de rangos aceptables para producción")
    else:
        print(f"   ✅ Excelente generalización (gap: {overfitting_gap:.4f})")
    
    print("\n🔍 IMPORTANCIA DE CARACTERÍSTICAS (Top 10):")
    best_model = grid_search.best_estimator_.named_steps['classifier']
    feature_names = (numeric_features + 
                    list(grid_search.best_estimator_.named_steps['preprocessor']
                         .named_transformers_['cat']
                         .named_steps['onehot']
                         .get_feature_names_out(categorical_features)))
    
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False).head(10)
    
    for idx, row in feature_importance.iterrows():
        print(f"   {row['feature']}: {row['importance']:.4f}")
    
except Exception as e:
    print(f"❌ ERROR durante el entrenamiento: {str(e)}")
    exit(1)

# ============================================================================
# GUARDAR MODELO Y METADATA
# ============================================================================
print("\n💾 GUARDANDO MODELO Y METADATA...")

try:
    os.makedirs('models', exist_ok=True)
    
    # Guardar pipeline optimizado
    joblib.dump(grid_search.best_estimator_, 'models/titanic_pipeline.pkl')
    print("✅ Pipeline guardado en 'models/titanic_pipeline.pkl'")
    
    # Crear metadata con información importante
    metadata = {
        'model_type': 'RandomForestClassifier',
        'features': features,
        'numeric_features': numeric_features,
        'categorical_features': categorical_features,
        'train_score': float(train_score),
        'validation_score': float(val_score),
        'best_params': {k: str(v) if not isinstance(v, (int, float, str, bool, type(None))) else v 
                       for k, v in grid_search.best_params_.items()},
        'cv_score': float(grid_search.best_score_),
        'classes': [0, 1],
        'class_names': ['No Sobrevive', 'Sobrevive'],
        'feature_ranges': {
            'Age': {'min': float(df['Age'].min()), 'max': float(df['Age'].max())},
            'Fare': {'min': float(df['Fare'].min()), 'max': float(df['Fare'].max())},
            'SibSp': {'min': int(df['SibSp'].min()), 'max': int(df['SibSp'].max())},
            'Parch': {'min': int(df['Parch'].min()), 'max': int(df['Parch'].max())}
        },
        'valid_values': {
            'Pclass': [1, 2, 3],
            'Sex': ['male', 'female'],
            'Embarked': ['C', 'Q', 'S']
        }
    }
    
    with open('models/model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print("✅ Metadata guardada en 'models/model_metadata.json'")
    
except Exception as e:
    print(f"❌ ERROR al guardar archivos: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 80)
print("🎉 PROCESO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print("\n📦 Archivos generados:")
print("   - models/titanic_pipeline.pkl (modelo entrenado)")
print("   - models/model_metadata.json (información del modelo)")
print("\n🚀 Siguiente paso: Ejecutar la API de Django")
