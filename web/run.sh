#! /bin/sh
### pwd = sender/web
redis-server &
celery -A web worker --loglevel=info --beat

