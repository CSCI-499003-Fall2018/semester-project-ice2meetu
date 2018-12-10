import os
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IceToMeetYou.settings")
channel_layer = get_default_application()