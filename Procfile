web: gunicorn titanic_api.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate && python scripts/01_data_analysis_and_training.py
