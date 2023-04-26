zhdhsadhjksdhskjahdk#sdffkshjdfkdhskfhsdhfisdfsd
#asdasjhdkashdhkj#wmfksdfljsdlkfjsdjklfjsdklfjsdkljfklsdjfklsjdflkjdsklfjsdljfskfjs;kdfsdkjdskj
#sdfjsdkfjsdklfsdkfjksjdkfjkjjskdjfkjsjdkfjsdjkfksdhfkhsjkfhsjkhfsdshfsldj
# import os,django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarShipping.settings")
# django.setup()
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
# OutstandingToken.objects.all().delete()
# list1 = [1,23,323,234,32]
# for value in list1[1:]:
#     print(value)
# # print(data)
#
# data = 'AAA BBB AA'
# print(set(data))
# sting = '({[]}){}'
# new_list = []
# backcount = 0
# print([i+j for i in "abc" for j in "def"])


# lef_parathnesis = ['(','{','[']
# right_parathnesis = [')','}',']']
# is_valid = ''
# stack = []
# for value in sting:
#     if value in lef_parathnesis:
#         stack.append(value)
#     elif value == ')' and stack!=[] and stack[-1]== '(':
#         stack.pop()
#     elif value == '}' and stack!=[] and stack[-1]== '{':
#         stack.pop()
#     elif value == ']' and stack!=[] and stack[-1]== '[':
#         stack.pop()
#     else:
#         is_valid = False
#         break
# if stack==[]:
#     is_valid = True
# else:
#     is_valid = False
# print(is_valid)
    # if len(sting)%2!=0:
    #     is_valid = False
    #     break
    # if sting[index] in lef_parathnesis:
    #     for index2 in range(index,len(sting)):
    #         if sting[index2] in right_parathnesis:
    #                 if ord(sting[index])== (ord(sting[index2])-1) or ord(sting[index]) ==(ord(sting[index2])-2):
    #                     if index2-index-1%2==0:
    #                         is_valid = True
# :

    #     new_list.append(value)
    #


# print(is_valid)

# )


# from rest_framework_simplejwt.models import auth_models
# from rest_framework.authtoken.models import Token
# data = Token.objects.all()
# print(data)

# from weasyprint import HTML, CSS
# from django.template.loader import get_template
#
# html_template = get_template('Invoice.html')
# pdf_file = HTML('/home/umer/Desktop/BPL/CarShipping_updated/CarShipping/chat/templates/Invoice.html').write_pdf("./butt.pdf")
#
# print(pdf_file)




# import requests
# #
# url = 'http://192.168.0.112:8000/invoice/'
#
#
# dic = {
#     "lead_id" : "LQT1232"
# }
#
# #
# response = requests.post(url,data=dic)
# print(response.status_code)
# print(type(response.content))
# # print(response.text)
# #
# #
# file = open('./butt.pdf','wb')
# file.write(response.content)
# file.close()
