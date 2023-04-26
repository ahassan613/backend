"""
ASGI config for CarShipping project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os
#
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import django
# import chat.routing
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarShipping.settings')
# django.setup()
#
# # application = get_asgi_application()
#
# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })
#
# import os
#
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import chat.routing
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#
# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# }
#
# )

# import sys
# # sys.path.append('/home/brainplow123/PycharmProjects/ShopnroarAmazon')
# sys.path.append('/usr/src/app/CarShipping')
# sys.path.append('/amazon/shopnroar_amazon/')
# import os, django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SNR.settings")
# django.setup()


# import os,django
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import chat.routing
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShipping.settings")
# # django.setup()
#
# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })
#

import os
import django
from channels.routing import get_default_application
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarShipping.settings')
django.setup()
application = get_default_application()

# import os
# import django
# from channels.routing import get_default_application
# from channels.layers import get_channel_layer
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dhaar2.settings")
# django.setup()
# application = get_default_application()
