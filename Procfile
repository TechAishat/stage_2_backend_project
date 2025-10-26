web: gunicorn --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --timeout 600 --bind :10000 config.wsgi:application
