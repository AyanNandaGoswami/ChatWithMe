web: daphne ChatWithMe.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=ChatWithMe.settings -v2