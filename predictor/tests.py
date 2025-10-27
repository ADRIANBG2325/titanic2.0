from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class PredictorAPITestCase(TestCase):
    """Tests para la API de predicción del Titanic"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_health_check(self):
        """Test del endpoint de health check"""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
    
    def test_predict_valid_data(self):
        """Test de predicción con datos válidos"""
        data = {
            'Pclass': 1,
            'Sex': 'female',
            'Age': 25,
            'SibSp': 0,
            'Parch': 0,
            'Fare': 50,
            'Embarked': 'S'
        }
        response = self.client.post('/api/predict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('prediccion', response.data)
    
    def test_predict_invalid_pclass(self):
        """Test con Pclass inválido"""
        data = {
            'Pclass': 5,  # Inválido
            'Sex': 'female',
            'Age': 25,
            'SibSp': 0,
            'Parch': 0,
            'Fare': 50,
            'Embarked': 'S'
        }
        response = self.client.post('/api/predict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_predict_missing_required_field(self):
        """Test con campo requerido faltante"""
        data = {
            'Pclass': 1,
            # Falta 'Sex'
            'Age': 25,
            'SibSp': 0,
            'Parch': 0,
            'Fare': 50,
            'Embarked': 'S'
        }
        response = self.client.post('/api/predict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
