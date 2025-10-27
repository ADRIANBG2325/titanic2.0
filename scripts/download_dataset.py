"""
Script para descargar el dataset de Titanic si no existe
Se ejecuta automáticamente durante el deployment
"""
import os
import urllib.request
import sys

def download_dataset():
    """Descarga el dataset de Titanic desde una fuente confiable"""
    
    print("Verificando dataset de Titanic...")
    
    # URLs del dataset
    TRAIN_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    
    # Verificar si train.csv ya existe
    if os.path.exists('train.csv'):
        print("Dataset encontrado localmente")
        return True
    
    print("Descargando dataset de Titanic...")
    try:
        urllib.request.urlretrieve(TRAIN_URL, 'train.csv')
        print("Dataset descargado exitosamente")
        return True
    except Exception as e:
        print(f"Error al descargar dataset: {str(e)}")
        print("Por favor, descarga manualmente desde: https://www.kaggle.com/c/titanic/data")
        return False

if __name__ == "__main__":
    success = download_dataset()
    sys.exit(0 if success else 1)
