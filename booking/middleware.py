import re


from django.utils.deprecation import MiddlewareMixin
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShipping.settings")
django.setup()
from rest_framework_simplejwt import authentication

from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
class PasswordUpdateCheck(MiddlewareMixin):
    def process_request(self, request):
        if '/login/' in str(request) or 'insertLeads/' in str(request):
            return
        try:
            username = authentication.JWTAuthentication().authenticate(request)[0]
        except:
            username = None
        if username!=None:
            if OutstandingToken.objects.filter(user__username=username).count() > 0:
                pass
            else:
                raise PermissionDenied


