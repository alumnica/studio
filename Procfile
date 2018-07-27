web: gunicorn studio_webapp.wsgi --log-file -
worker: python -c 'from django_h5p import worker; worker.main()'