#! /bin/sh
### pwd = sender/web
celery -A web worker --loglevel=info --beat
redis-server
