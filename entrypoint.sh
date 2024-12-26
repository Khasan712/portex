#set -o errexit
#set -o pipefail
#set -o nounset

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:9000
#gunicorn config.wsgi:application --bind 0.0.0.0:8001 --workers 4 --timeout 120 --reload --worker-class gevent --max-requests 1000 --max-requests-jitter 100