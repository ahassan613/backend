# from django.test import TestCase
#
# # Create your tests here.
#
# # Receive message from WebSocket
# async def receive(self, text_data):
#     print("in recive")
#     text_data_json = json.loads(text_data)
#     if 'Typing' in text_data_json:
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'Typing': text_data_json['Typing'],
#                 # 'username':text_data_json['username']
#             }
#         )
#     else:
#         room = self.room_name
#         if room:
#             # user = User.objects.get(username=username)
#             pass
#             # Messages.objects.create(room_name=room,sender=text_data_json['username'],receiver=text_data_json['receiver'],message=text_data_json['message'])
#         message = text_data_json['message']
#         # username = text_data_json['username']
#         # status = text_data_json['status']
#         # receiver = text_data_json['receiver']
#
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'room_name': self.room_group_name
#                 # 'sender' : username,
#                 # 'receiver' : receiver,
#                 # 'status': status
#             }
#
#         )
#
# import gateway
# import MerchantInfo
# data = {'merchantKey': 'merchantKey',
#     'processorId': 'processorId'
#     #See attributes
# }
# RestGateway = gateway.RestGateway(data)
# RestGateway.createSale()
# def SuccessHandler(result, status):
#     #See Return
#     pass
# def ErrorHandler(result, status):
#     #See Error Handling
#     pass
# def ValidationHandler(result, status):
#     pass
#
# print('hello world')

import requests
url = 'https://secure.1stpaygateway.net/secure/RestGW/Gateway/Transaction/Sale'
# url = 'https://secure.merchantonegateway.com/api/transact.php?username=mfarooq75023&password=brainplow786@lahore&type=sale&ccnumber=' + str(
#     creditno) + '&ccexp=' + str(exp_date) + '&cvv=' + str(cvv) + '&amount=' + str(
#     amount) + '&descriptor=Quantum Transport Solution.'
exp_date='06/24'
e_date=exp_date.split('/')
month=e_date[0]
year=e_date[1]

payload = {
    "merchantKey": "984b2d4d-bbc5-41db-9767-69c61e852f92",
    "processorId": "329513",
    "cardNumber": "5563053703478518",
    "cardExpMonth": month,
    "cardExpYear": year,
    "transactionAmount": "951",
    "ownerName": "John Stelle",
    "ownerStreet": "5401 North Central Expy",
    "ownerCity": "Dallas",
    "ownerState": "TX",
    "ownerZip": "75205",
    "cVV": "420"

}
# result 201
# result {"data":{"authResponse":"APPROVED","authCode":"805378",
# "referenceNumber":"255467236","isPartial":false,"partialId":"","originalFullAmount":0.01,
# "partialAmountApproved":0.0,"avsResponse":"G","cvv2Response":"M",
# "orderId":"637848939119523805",
#                 "cardType":"Visa","last4":"1698","maskedPan":"464951******1698",
#                 "token":"2691199889191698","hasFee":false,"fee":null},"isError":false,
#         "errorMessages":[],"validationHasFailed":false,"validationFailures":[],
#         "isSuccess":true,"action":"Sale"}
#CVV EROOR
# result 400
# result {"data":{"authResponse":"TRANS DENIED DO NOT HONOR",
# "authCode":"","referenceNumber":"255467502","isPartial":false,"partialId":"
# ","originalFullAmount":0.01,"partialAmountApproved":0.0,"avsResponse":"G","cvv2Response"
# :"N","orderId":"","cardType":"Visa","last4":"1698","maskedPan":"464951******1698",
# "token":"2691199889191698","hasFee":false,"fee":null},"isError":true,"errorMessages"
# :["TRANS DENIED DO NOT HONOR"],"validationHasFailed":false,"validationFailures":[],
# "isSuccess":false,"action":"Sale"}

##Date
# result 400
# result {"data":{"authResponse":"TRANS DENIED DO NOT HONOR","authCode":
# "","referenceNumber":"255468186","isPartial":false,"partialId":"",
# "originalFullAmount":0.01,"partialAmountApproved":0.0,"avsResponse":"G","
# cvv2Response":"N","orderId":"","cardType":"Visa","last4":"1698","maskedPan":
# "464951******1698","token":"2691199889191698","hasFee":false,"fee":null},"isError":true,
# "errorMessages":["TRANS DENIED DO NOT HONOR"],"validationHasFailed":false,
# "validationFailures":[],"isSuccess":false,"action":"Sale"}

##Wrong Card Number
# result 400
# result {"data":{"authResponse":"","authCode":"","referenceNumber":"",
# "isPartial":false,"partialId":"","originalFullAmount":0.0,"partialAmountApproved"
# :0.0,"avsResponse":"","cvv2Response":"","orderId":"","cardType":null,"last4":null,
# "maskedPan":null,"token":null,"hasFee":false,"fee":null},"isError":false,
# "errorMessages":[],"validationHasFailed":true,"validationFailures"
# :[{"key":"cardNumber","message":"Credit card number entered is not valid"}],
# "isSuccess":false,"action":"Sale"}



r = requests.post(url, data=payload)
code = r.text
# print("result", r.status_code)
# print("result", r.text)
response_text = code.split('authCode')
#
# print("split1", response_text[0])
#
if '"authResponse":"APPROVED"' in response_text[0] or 'Approved' in response_text[0]:
    print("Sucess")
    status_text = 'Valid'
    # if request.data['partial_fee'] == book_obj.booking_fee:
    #     book_obj.fee_status = True
    #     book_obj.payment_response = r.text
    #     book_obj.save()
    # else:
    #     remaning_payment = float(book_obj.booking_fee) - float(request.data['partial_fee'])
    #     PartialPayment.objects.create(
    #         booking_id=book_obj,
    #         partial_fee=request.data['partial_fee'],
    #         payment_response=r.text
    #     )
    #     book_obj.remaning_fee = remaning_payment
    #     book_obj.save()
    #
    # return Response({"message": "Payment Done succesffully"}, status=status.HTTP_200_OK)

elif 'Credit card number entered is not valid' in response_text[1]:
    print("Credit card number wrong")
    # status_text = 'Invalid Credit Card'
    # return Response({"message": "Invalid Card Number"}, status=status.HTTP_400_BAD_REQUEST)

elif 'TRANS DENIED DO NOT HONOR' in response_text[1]:
    print("cvv or exp wrong")
    status_text = 'Invalid cvv or exp'
    # return Response({"message": "Invalid Cvv or Expiry"}, status=status.HTTP_400_BAD_REQUEST)
else:
    print("something went wrong")