web: gunicorn studio_webapp.wsgi --log-file -
worker: python -c 'from studio_webapp import worker; worker.main()'