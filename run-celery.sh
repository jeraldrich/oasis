alias activate=". .venv/bin/activate" 
activate && cd app && celery worker -A app.celery --loglevel=info
