"""
WSGI config for catalogproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

print("MY_WEBSITE_HOSTNAME:", os.environ.get('MY_WEBSITE_HOSTNAME'))

settings_module = 'catalogproject.deployment' if 'MY_WEBSITE_HOSTNAME' in os.environ else 'catalogproject.settings'
print("Using settings module:", settings_module)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catalogproject.deployment')

application = get_wsgi_application()