import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShipping.settings")
django.setup()

from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from booking.views import *

# user_obj =User.objects.get(username='azhar613')
# print(user_obj)

# data=Leads.objects.filter(received_date__date__lt='2022-01-20',assigned_to=None).update(assigned_to=user_obj)
# print(data.count())
from datetime import datetime
import pytz

tz = pytz.timezone('America/Panama')

print(datetime.now(tz))
print(datetime.utcnow())
# lead_ob = Leads.objects.get(id=27792)
# print(lead_ob.received_date)import traceback
from bs4 import BeautifulSoup
import  requests
import re
import math
import sys


sys.path.append('/home/brainplow/Documents/shopnroar_amazon')


# sys.path.append('/amazon/shopnroar_amazon/')
import os, django
from selenium.webdriver.common.keys import Keys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SNR.settings")
django.setup()
# for value in data:
#     print(value.received_date)

# data = OutstandingToken.objects.filter(user__username='umer').count()
# print(data)


from booking.models import *

# data=Leads.objects.filter(payment_id='LQT5126')
# for val in data:
#     print(val.payment_response)
