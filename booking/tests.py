# # from django.test import TestCase
# # import traceback
# # import  requests
# # import re
# # import math
# # import sys
# #
# #
# # sys.path.append('/home/brainplow/azhar/quantum/QuantumBackend_1stSep/QuantumBackend/booking')
# #
# #
# # # sys.path.append('/amazon/shopnroar_amazon/')
# # import os, django
# # # from selenium.webdriver.common.keys import Keys
# # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShipping.settings")
# # django.setup()
# # from booking.models import *
# #
# # # all_objs = Leads.objects.filter(SNR_Active=True, SNR_Available='hollar')
# # all_objs = Leads.objects.get(id=595556)
# # print(all_objs.received_by)
# # print(all_objs.count())
# # # for obj in all_objs:
# #
# #
# # # Create your tests here.
# # lis =[15,6,8,1,3]
# #
# import traceback
# import  requests
# import re
# import math
# import sys
#
#
# sys.path.append('/home/brainplow/azhar/quantum/QuantumBackend_1stSep/QuantumBackend')
#
#
# # sys.path.append('/amazon/shopnroar_amazon/')
# import os, django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShipping.settings")
# django.setup()
# from booking.models import Leads,UserRole
# from django.contrib.auth.models import User
#
#
#
#
#
# # # all_objs = Leads.objects.filter(SNR_Active=True, SNR_Available='hollar')
# # all_objs = Leads.objects.get(id='59556')
# # print(all_objs.received_by)
# # user = User.objects.create_user(username='john',
# #                                  email='qts@testing.com',
# #                                  password='goquantum')
# user_obj = User.objects.get(username='john')
# # roleobj = UserRole.objects.get(user_id_id=request.user.id)
# print('Done')
# UserRole.objects.create(
#     user_id=user_obj,
#     role='S'
# )
# print('Done')

lis=[0,1,2,3]
print(lis[-len(lis)])