"""
WSGI config for shortdra_eb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

sys.path.insert(0, '/opt/python/current/app')

os.environ['DJANGO_SETTINGS_MODULE'] = 'shortdra_eb.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
