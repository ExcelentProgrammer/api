# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/home/api.iprogrammer.uz/config')
sys.path.insert(1, '/home/api.iprogrammer.uz/venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
