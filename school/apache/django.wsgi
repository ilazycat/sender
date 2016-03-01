import os

import sys

path = '/home/lc4t/web_py/school'

if path not in sys.path:

    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'school.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
