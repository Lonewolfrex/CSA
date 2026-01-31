"""
CSA Library WSGI config for Django
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csa.settings.development')

application = get_wsgi_application()
