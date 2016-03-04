"""
WSGI config for school project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
sys.path.append('/home/sender/web_py/school')
application = get_wsgi_application()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# os.environ['LC_ALL']="en_US.UTF-8"
