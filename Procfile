web: gunicorn --worker-class=sync --workers=1 --timeout=120 --access-logfile - --error-logfile - --bind 0.0.0.0:$PORT src.app:app
