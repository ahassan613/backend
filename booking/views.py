import json

from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status,permissions
import requests
from django.core.mail.message import EmailMessage
from datetime import datetime
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from django.db.models import Q
# Create your views here.
import after_response
from django.template.loader import get_template
from django.db import connection
from rest_framework import mixins,generics
from clients import twilio_client

# from django.shortcuts import render, redirect

# from clients import twilio_client
# from .forms import VerificationForm, TokenForm






@after_response.enable
def emailsending_admin(key,template,msg):
    key['datetime'] = datetime.now()
    message = get_template(template).render(key)
    email = EmailMessage(msg, message, to=['azharhassan613@gmail.com','quantumtransportsolns@gmail.com','omar.farooq1012@gmail.com'])
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')


@after_response.enable
def emailsending_users(key,template,subject,user_email,user_obj,emailfrom):
    key['datetime'] = datetime.now()
    key['username'] = user_obj.first_name
    # key['user_email'] = user_email
    key['user_email'] = emailfrom
    key['user_phone'] = user_obj.last_name
    try:
        key['price'] = str(key['price']).split('.')[0]
    except:
        pass
    message = get_template(template).render(key)
    tolist = []
    tolist.append(key['email'])
    email = EmailMessage(subject, message, from_email=user_obj.first_name+' <'+emailfrom+'>', to=tolist)
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')


@after_response.enable
def emailsending_quantumadmin(key,template,msg):
    print(key)
    key['datetime'] = datetime.now()
    message = get_template(template).render(key)
    email = EmailMessage(msg, message, to=['azharhassan613@gmail.com','quantumtransportsolns@gmail.com','omar.farooq1012@gmail.com'])
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')


@after_response.enable
def emailsending_payment(key,template,msg,card_no,card_holder_name,amount):
    new_key = {
        "card_no" : card_no,
        "card_holder_name" : card_holder_name,
        "payment_id": key.payment_id,
        "amount": amount
    }
    message = get_template(template).render(new_key)
    email = EmailMessage(msg, message, to=['omar.farooq1012@gmail.com','azharhassan613@gmail.com','qsh.payments@leadsequity.com'])
    # email = EmailMessage(msg, message, to=['umarzafar54@gmail.com'])
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')


@after_response.enable
def emailsending_agent(key,template,msg,user_obj):

    message = get_template(template).render(key)
    email = EmailMessage(msg, message, to=[user_obj.email])
    email.content_subtype = 'html'
    email.send()
    print('Email Send Successfully')

@after_response.enable
def bulk_assing_email(key,template,msg,user_obj):
    new_key = {
        "value": key
    }
    message = get_template(template).render(new_key)
    email = EmailMessage(msg,message,to=[user_obj.email])
    email.content_subtype = 'html'
    email.send()
    print("email ensss")










{
    "name" : "samrock",
    "email" : "abc@gmail.com",
    "phone" : "3321213",
    "pick_up" : "75001",
    "drop_off" : "75002",
    "pick_up_date" : "2021-10-15",
    "type_of_service" : "Open",
    "vehicle_run" : True,
    "make": "Toyota",
    "model" : "Yaris",
    "Year" : "2021"
    }
@permission_classes((permissions.AllowAny,))
class AddBooking(APIView):
    def post(self,request):

        booking_serializer = BookingSerializer1(data=request.data)
        try:
            lead_data={}
            lead_data['full_name']=request.data['name']
            lead_data['email'] = request.data['email']
            lead_data['phone'] = request.data['phone']
            lead_data['origin_city'] = request.data['pick_up']
            lead_data['origin_state'] = request.data['pick_up']
            lead_data['origin_zip'] = request.data['pick_up']
            lead_data['destination_city'] = request.data['drop_off']
            lead_data['destination_state'] = request.data['drop_off']
            lead_data['destination_zip'] = request.data['drop_off']
            lead_data['ship_date1'] = request.data['pick_up_date']

            lead_data['car_maker'] = request.data['make']
            lead_data['car_model'] = request.data['model']
            lead_data['model_year1'] = request.data['year']
            lead_data['body_type'] = 'NA'
            if request.data['vehicle_run']:
                lead_data['vehilce_run1'] = 'Yes'
            else:
                lead_data['vehilce_run1'] = 'No'
            lead_data['transport_type1'] = request.data['type_of_service']
            lead_data['price'] = '0'
            lead_data['received_by'] = "QTS Lead"
            if not Leads.objects.filter(origin_zip=lead_data['origin_zip'],
                                        destination_zip=lead_data['destination_zip'],
                                        car_maker=lead_data['car_maker'], car_model=lead_data['car_model']).exists():
                serizl_obj = LeadsSerializer1(data=lead_data)
                if serizl_obj.is_valid():
                    resp = serizl_obj.save()
                    resp.payment_id = 'LQT' + str(1000 + resp.id)
                    resp.save()
                    print('All ok yar')

                else:
                    print('Issue in Serializer')


        except:
                print('Error in Book to Lead ')
        if booking_serializer.is_valid():
            booking_serializer.save()
            emailsending_quantumadmin.after_response(booking_serializer.data, 'quantum_booking.html',
                                              'QTS Lead Generated')
            return Response({"messasge":"Data Saved"},status=status.HTTP_201_CREATED)
        return Response(booking_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class GetBookings(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0
        total_items = Booking.objects.all().count()
        bookoing_obj = Booking.objects.all()[start:offsetlimit]
        serail_obj = BookingSerializer(bookoing_obj,many=True)
        result = {
            "total_items" : total_items,
            "results" : serail_obj.data
        }

        return Response(result,status=status.HTTP_200_OK)


{
    "agent_id": 1,
    "booking_id" : 1,

}

class AssignBooking(APIView):
    def put(self,request):
        if User.objects.filter(id=request.data['agent_id']).exists():
            if Booking.objects.filter(id=request.data['booking_id']).exists():
                agent_obj=User.objects.get(id=request.data['agent_id'])
                Booking.objects.filter(id=request.data['booking_id']).update(assigned_to=agent_obj)
                return Response({"message":"Assigned Successfuly"},status=status.HTTP_200_OK)
            return Response({"message":"Booking does not exists"})
        return Response({"message":"You enter wrong user id"},status=status.HTTP_400_BAD_REQUEST)


{

    "agent_user_id" : "umer333",
    "booking_id" : 1,
    "booking_fee" : 120,
    "truck_name": "sam",
    "truck_no": "Abc13",
    "trucker_license": "iu123"
 }

class ConfirmBooking(APIView):
    def post(self,request):
        if User.objects.filter(id=request.data['agent_user_id']).exists():
            # agent_obj = AgentDetail.objects.get(agent_id=request.data['agent_id'])
            book_obj = Booking.objects.get(id=request.data['booking_id'])
            confirm_obj = ConfirmBook()
            confirm_obj.booking_id= book_obj
            confirm_obj.booking_fee=request.data['booking_fee']
            confirm_obj.truck_no = request.data['truck_no']
            confirm_obj.truck_name = request.data['truck_name']
            confirm_obj.trucker_license=request.data['trucker_license']
            confirm_obj.remaning_fee = request.data['booking_fee']
            confirm_obj.save()
            confirm_obj.order_id = 'QT'+str(confirm_obj.id + 1000)
            confirm_obj.save()
            return Response({"message":"Order booked sucessfully"},status=status.HTTP_200_OK)
        return Response({"message": "User not exists"}, status=status.HTTP_400_BAD_REQUEST)



{
    "username" : "Zayan333",
    "full_name" : "Zayan ul haq",
    "password": "123456",
    "email" : "abc@gmail.com",
    "phone": "123212"
}

class AddAgent(APIView):

    def post(self,request):
        phone = ""
        if 'phone' in request.data.keys():
            phone = request.data['phone']
        if User.objects.filter(username=request.data['username']).exists():
            return Response({"message":"Username already exists"},status=status.HTTP_400_BAD_REQUEST)
        userobj = User(
            username= request.data['username'],
            first_name = request.data['full_name'],
            email= request.data['email'],
            last_name=phone
        )
        userobj.set_password(request.data['password'])
        userobj.save()
        UserRole.objects.create(
            user_id=userobj,
            role='A'
        )
        return Response({'message':"Agent Created Successfully"},status=status.HTTP_201_CREATED)

{
    "id":123,
    "full_name": "umer zafar",
    "phone": "239810381",
    "password": "12312",
    "username" : "sabc123",
    "email": "abc@gmail.com"
}


class UpdateAgent(APIView):
    def post(self,request):
        try:
            user_obj = User.objects.get(id=request.data['id'])
            user_obj.first_name = request.data['full_name']
            user_obj.last_name = request.data['phone']
            user_obj.username = request.data['username']
            user_obj.email = request.data['email']
            user_obj.save()
            if request.data['password']!=None:
                user_obj.set_password(request.data['password'])
                user_obj.save()
                OutstandingToken.objects.filter(user=user_obj).delete()


            return Response({"message":"Data Updated successfully"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":e},status=status.HTTP_400_BAD_REQUEST)


{
    "order_id":1001,
    "card_no": 12312312312,
    "cvv" : "23",
    "expiry_date" : "20/12",
}
@permission_classes((permissions.AllowAny,))
class Payment(APIView):
    def post(self,request):
        order = request.data['order_id']
        book_obj = None
        fee_status = None
        amount = None
        Order_check = 0
        if 'QT' == order[0:2]:
            if ConfirmBook.objects.filter(order_id=request.data['order_id']).exists():
                book_obj = ConfirmBook.objects.get(order_id=request.data['order_id'])
                fee_status = book_obj.fee_status
                amount = book_obj.remaning_fee
                Order_check =1
        elif 'LQT' == order[0:3]:
            if Leads.objects.filter(payment_id=request.data['order_id']).exists():
                book_obj = Leads.objects.get(payment_id=request.data['order_id'])
                fee_status = book_obj.is_paid
                amount = book_obj.agent_price
                Order_check =2
        else:
            if JTrackerConfirmBook.objects.filter(jTracker_id=request.data['order_id']).exists():
                book_obj = JTrackerConfirmBook.objects.get(jTracker_id=request.data['order_id'])
                fee_status = book_obj.payment_status
                amount = book_obj.dispatch_fee
                Order_check = 3
        if book_obj == None:
            return Response({"message":"Payment not found"},status=status.HTTP_404_NOT_FOUND)
        else:
            # book_obj = ConfirmBook.objects.get(order_id=request.data['order_id'])
            # book_obj= book_obj[0]
            print("after get")
            if fee_status==False:
                cvv = request.data['cvv']
                exp_date = request.data['expiry_date']
                e_date = exp_date.split('/')
                month = e_date[0]
                year = e_date[1]
                creditno =  request.data['card_no']
                url='https://secure.1stpaygateway.net/secure/RestGW/Gateway/Transaction/Sale'
                # url = 'https://secure.merchantonegateway.com/api/transact.php?username=mfarooq75023&password=brainplow786@lahore&type=sale&ccnumber=' + str(
                #     creditno) + '&ccexp=' + str(exp_date) + '&cvv=' + str(cvv) + '&amount=' + str(
                #     amount) + '&descriptor=Quantum Transport Solution.'

                if 'owner_name' in request.data.keys():
                    owner_name = request.data['owner_name']
                else:
                    owner_name = 'Tariq Farooq'
                payload = {
                    "merchantKey": "984b2d4d-bbc5-41db-9767-69c61e852f92",
                    "processorId": "329513",
                    "cardNumber": creditno,
                    "cardExpMonth": month,
                    "cardExpYear": year,
                    "transactionAmount": amount,
                    "ownerName": owner_name,
                    "ownerStreet": "Echo Trl",
                    "ownerCity": "Dallas",
                    "ownerState": "TX",
                    "ownerZip": "75023",
                    "cVV": cvv

                }

                r = requests.post(url, data=payload)
                code = r.text
                print("result", r.status_code)
                print("result", r.text)

                response_text = code.split('authCode')
                #
                # print("split1", response_text[0])

                if '"authResponse":"APPROVED"' in response_text[0] or 'Approved' in response_text[0]:
                    print("Sucess")
                    if Order_check==1:
                        status_text = 'Valid'
                        book_obj.fee_status = True
                        book_obj.payment_response = r.text
                        book_obj.save()
                    elif Order_check==2:
                        book_obj.is_paid = True
                        try:
                            book_obj.payment_response = r.text

                        except:
                            pass
                        try:
                            book_obj.payment_date = str(datetime.now())
                        except:
                            pass
                        book_obj.save()

                    elif Order_check==3:
                        book_obj.payment_status = True

                        book_obj.save()
                        # (key, template, msg, card_no, card_holder_name, amount)
                    msg = f'${str(amount)} Credit Card Payment Received from {owner_name}'
                    new_credit = str(creditno)[-4:]
                    emailsending_payment.after_response(book_obj, 'payment_notification.html', msg, new_credit, owner_name, amount)
                    return Response({"message":"Payment Done succesffully"},status=status.HTTP_200_OK)

                elif 'Credit card number entered is not valid' in response_text[1]:
                    print("Credit card number wrong")
                    # status_text = 'Invalid Credit Card'
                    return Response({"message": "Invalid Card Number"}, status=status.HTTP_400_BAD_REQUEST)

                elif 'TRANS DENIED DO NOT HONOR' in response_text[1]:
                    print("cvv or exp wrong")
                    status_text = 'Invalid cvv or exp'
                    return Response({"message": "Invalid Cvv or Expiry"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    print("something went wrong")
                    return Response({"message": "Something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"Payment Already Paid Against this order id"},status=status.HTTP_403_FORBIDDEN)
        # return Response({"message": "No Order id found"}, status=status.HTTP_404_NOT_FOUND)


{
    "order_id":1001,
    "card_no": 12312312312,
    "cvv" : "23",
    "expiry_date" : "20/12",
    "partial_fee" : 10
}
@permission_classes((permissions.AllowAny,))
class PartialPayment(APIView):
    def post(self,request):

        if ConfirmBook.objects.filter(order_id=request.data['order_id']):
            book_obj = ConfirmBook.objects.get(order_id=request.data['order_id'])
            if float(request.data['partial_fee'])<=float(book_obj.remaning_fee):
                if book_obj.fee_status==False:
                    cvv = request.data['cvv']
                    exp_date = request.data['expiry_date']
                    e_date = exp_date.split('/')
                    month = e_date[0]
                    year = e_date[1]
                    creditno =  request.data['card_no']
                    amount = request.data['partial_fee']
                    amount = '00.00'
                    # url = 'https://secure.merchantonegateway.com/api/transact.php?username=mfarooq75023&password=brainplow786@lahore&type=sale&ccnumber=' + str(
                    #     creditno) + '&ccexp=' + str(exp_date) + '&cvv=' + str(cvv) + '&amount=' + str(
                    #     amount) + '&descriptor=Quantum Transport Solution.'
                    url = 'https://secure.1stpaygateway.net/secure/RestGW/Gateway/Transaction/Sale'
                    print(url)
                    payload = {
                        "merchantKey": "984b2d4d-bbc5-41db-9767-69c61e852f92",
                        "processorId": "329513",
                        "cardNumber": creditno,
                        "cardExpMonth": month,
                        "cardExpYear": year,
                        "transactionAmount": amount,
                        "ownerName": "Tariq Farooq",
                        "ownerStreet": "Echo Trl",
                        "ownerCity": "Dallas",
                        "ownerState": "TX",
                        "ownerZip": "75023",
                        "cVV": cvv

                    }
                    r = requests.post(url, data=payload)
                    code = r.text
                    print("result", r.status_code)
                    print("result", r.text)

                    response_text = code.split('authCode')

                    print("split1", response_text[1])

                    if '"authResponse":"APPROVED"' in response_text[0] or 'Approved' in response_text[0]:
                        print("Sucess")
                        status_text = 'Valid'
                        if request.data['partial_fee'] == book_obj.booking_fee:
                            book_obj.fee_status = True
                            book_obj.payment_response = r.text
                            book_obj.save()
                        else:
                            remaning_payment =float(book_obj.booking_fee) - float(request.data['partial_fee'])
                            PartialPayment.objects.create(
                                booking_id=book_obj,
                                partial_fee=request.data['partial_fee'],
                                payment_response=r.text
                            )
                            book_obj.remaning_fee = remaning_payment
                            book_obj.save()



                        return Response({"message":"Payment Done succesffully"},status=status.HTTP_200_OK)

                    elif 'Credit card number entered is not valid' in response_text[1]:
                        print("Credit card number wrong")
                        # status_text = 'Invalid Credit Card'
                        return Response({"message": "Invalid Card Number"}, status=status.HTTP_400_BAD_REQUEST)

                    elif 'TRANS DENIED DO NOT HONOR' in response_text[1]:
                        print("cvv or exp wrong")
                        status_text = 'Invalid cvv or exp'
                        return Response({"message": "Invalid Cvv or Expiry"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        print("something went wrong")
                        return Response({"message": "Something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message":"Payment Already Paid Against this order id"},status=status.HTTP_403_FORBIDDEN)
            return Response({"message":"You enter more payment than fee"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "No Order id found"}, status=status.HTTP_404_NOT_FOUND)

{
    "order_id" : 1001
}
@permission_classes((permissions.AllowAny,))
class GetPayment(APIView):
    def post(self,request):
        order = request.data['order_id']
        if 'QT' == order[0:2]:
            if ConfirmBook.objects.filter(order_id=request.data['order_id']).exists():
                book_obj = ConfirmBook.objects.get(order_id=request.data['order_id'])
                if book_obj.fee_status==False:
                    return Response({'payment_fee':book_obj.remaning_fee,'partial_allowed':book_obj.partial_payment_allowed},status=status.HTTP_200_OK)
                return Response({'message':'Payment already Paid'},status=status.HTTP_403_FORBIDDEN)
            return Response({"message":"No detail found against this order id"},status=status.HTTP_400_BAD_REQUEST)
        elif 'LQT' == order[0:3]:
            if Leads.objects.filter(payment_id=request.data['order_id']).exists():
                book_obj = Leads.objects.get(payment_id=request.data['order_id'])
                if book_obj.is_paid==False:
                    return Response({'payment_fee':book_obj.agent_price,'partial_allowed':False},status=status.HTTP_200_OK)
                return Response({'message':'Payment already Paid'},status=status.HTTP_403_FORBIDDEN)
            return Response({"message":"No detail found against this order id"},status=status.HTTP_400_BAD_REQUEST)




        else:
            if JTrackerConfirmBook.objects.filter(jTracker_id=request.data['order_id']).exists():
                book_obj = JTrackerConfirmBook.objects.get(jTracker_id=request.data['order_id'])
                if book_obj.payment_status == False:
                    return Response(
                        {'payment_fee': book_obj.dispatch_fee, 'partial_allowed': False},
                        status=status.HTTP_200_OK)
                return Response({'message': 'Payment already Paid'}, status=status.HTTP_403_FORBIDDEN)
            return Response({"message": "No detail found against this order id"}, status=status.HTTP_400_BAD_REQUEST)



@permission_classes((permissions.AllowAny,))
class Contact(APIView):
    def post(self,request):
        contact_seral = ConatctusSerializer(data=request.data)
        if contact_seral.is_valid():
            contact_seral.save()
            return Response({"messasge": "Data Saved"}, status=status.HTTP_201_CREATED)
        return Response(contact_seral.errors, status=status.HTTP_400_BAD_REQUEST)



class ContactMessages(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0
        total_obj=ContactUs.objects.all().count()
        bookoing_obj = ContactUs.objects.all().order_by('-id')[start:offsetlimit]
        serail_obj = ConatctusSerializer(bookoing_obj,many=True)
        result = {
            "total_items" : total_obj,
            "data" : serail_obj.data
        }
        return Response(result,status=status.HTTP_200_OK)



{
"full_name" :"umer zafar",
"email" :"abc@gmail.com",
    "phone" : "5313122",
    "origin_address" :"5th ave",
    "origin_city" : "Plano",
    "origin_state" : "Texas",
    "origin_zip" : "75023",
    "destination_address" :"7th Ave",
    "destination_city" : "New York",
    "destination_state" : "New York",
    "destination_zip" : "75225",
    "car_maker" : "",
    "car_model" : "Toyota",
    "body_type" : "Sedan"
}





class AddLeads(APIView):
    def post(self,request):
        leads_serializer = LeadsSerializer1(data=request.data)
        if leads_serializer.is_valid():
            leads_serializer.save()
            return Response(leads_serializer.data,status=status.HTTP_201_CREATED)
        return Response(leads_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#Ok not Ok
#assigned_to
#received_from
#lead_Status
#Date
{
    "is_ok" : None,
    "assigned_to" : None,
    "received_from" : None,
    "start_date" : "2021-12-01",
    "end_date" : "2021-12-03",
    "lead_status" : "Quote",
    "full_name" : "Sam",
    "assigend_status" : None,
    "lead_id": None

}
# @permission_classes((permissions.AllowAny,))
class LeadsDetail(APIView):
    def post(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 50
            start = offsetlimit - 50
        else:
            offsetlimit = 50
            start = 0

        q1 = Q()
        # q2 = Q()
        # this_one = 2
        user_obj = UserRole.objects.get(user_id__username='umer')
        # user_obj = UserRole.objects.get(user_id__id=request.user.id)
        if user_obj.role=='A':
            print("this is agent")
            q1 &= Q(assigned_to__id=request.user.id)
            if request.data['lead_status'] == 'Leads':
                q1 &= Q(lead_status=None)
                # q2 |= Q(lead_status="")
                # this_one=4
            else:
                q1 &= Q(lead_status=request.data['lead_status'])
        else:
            if request.data['lead_status'] != None and request.data['lead_status'] != "":
                q1 &= Q(lead_status=request.data['lead_status'])





        if 'lead_id' in request.data.keys():
            if request.data['lead_id']!=None and request.data['lead_id']!="":
                print("in payment")
                q1 &= Q(payment_id=request.data['lead_id'])

        if 'assigend_status' in request.data.keys():

            if request.data['assigend_status']!=None:
                if request.data['assigend_status']=='Unassigned':
                    q1 &= Q(assigned_to=None)
                if request.data['assigend_status']=='Assigned':
                    q1 &= ~Q(assigned_to=None)
        if request.data['is_ok']!=None:
            q1 &= Q(is_ok=request.data['is_ok'])
        if request.data['assigned_to'] !=None:
            print("in user")
            q1 &= Q(assigned_to=request.data['assigned_to'])
        if request.data['received_from'] != None:
            q1 &= Q(received_by__istartswith=request.data['received_from'])
        if request.data['start_date']!=None:
            q1 &= Q(received_date__date__gte=request.data['start_date'])
        if request.data['end_date']!=None:
            q1 &= Q(received_date__date__lte=request.data['end_date'])

        if 'full_name' in request.data.keys():
            if request.data['full_name']!=None:
                q1 &= Q(full_name__icontains=request.data['full_name'])
        print(q1)

        total_obj = Leads.objects.filter(q1).count()
        main_obj = Leads.objects.filter(q1).select_related('assigned_to').order_by('-id')[start:offsetlimit]
        # total_obj = main_obj.count()
        # leads_obj = main_obj[start:offsetlimit]
        serail_obj = LeadsSerializer(main_obj,many=True)
        result = {
            "total_items" : total_obj,
            "data" : serail_obj.data
        }
        return Response(result,status=status.HTTP_200_OK)


class GetAgents(APIView):
    def get(self,request):
        role_obj = UserRole.objects.filter(role='A',).order_by('-id').select_related('user_id')
        role_serial = roleSerializer(role_obj,many=True)
        return Response(role_serial.data,status=status.HTTP_200_OK)


class GetAgentsFast(APIView):

    def get(self,request):

        user_obj = User.objects.filter(samrock__role='A')
        serial_obj = UserSerializer(user_obj, many=True)
        return Response(serial_obj.data, status=status.HTTP_200_OK)






{
    "agent_id" : "umer333",
    "contact_id": 1,
    "agent_password" : "bpl321"
}

class LockContact(APIView):
    def put(self,request):
        if AgentDetail.objects.filter(agent_id=request.data['agent_id']).exists():
            if ContactUs.objects.filter(id=request.data['contact_id']).exists():
                agent_obj=AgentDetail.objects.get(agent_id=request.data['agent_id'])
                if agent_obj.agent_password == request.data['agent_password']:
                    ContactUs.objects.filter(id=request.data['contact_id']).update(locked=True,locked_by=agent_obj)

                    return Response({"message":"locked Successfuly"},status=status.HTTP_200_OK)
                return Response({"message":"Please enter correct agent password"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"Contact does not exists"})
        return Response({"message":"You enter wrong user id"},status=status.HTTP_400_BAD_REQUEST)


class TestBooking(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0
        print(start)
        print(offsetlimit)
        role_obj = UserRole.objects.get(user_id=request.user.id)
        if role_obj.role =='S':
            total_items = Booking.objects.all().count()
            bookoing_obj = Booking.objects.all().order_by('-id')[start:offsetlimit]
        else:
            total_items = Booking.objects.filter(assigned_to__id=request.user.id).count()
            bookoing_obj = Booking.objects.filter(assigned_to__id=request.user.id).order_by('-id')[start:offsetlimit]
        serail_obj = BookingSerializer(bookoing_obj,many=True)
        result = {
            "total_items" : total_items,
            "results" : serail_obj.data
        }
        # print(serail_obj.data)

        return Response(result,status=status.HTTP_200_OK)
{
    "agent_id":"umer333",
    "order_id": "1001",
    "agent_password": "133"

}


class PartialAllowPayment(APIView):
    def put(self,request):
        if AgentDetail.objects.filter(agent_id=request.data['agent_id']).exists():
            if ConfirmBook.objects.filter(order_id=request.data['order_id']).exists():
                bookobj = ConfirmBook.objects.get(order_id=request.data['order_id'])
                agent_obj = AgentDetail.objects.get(agent_id=request.data['agent_id'])
                # if agent_obj.agent_password == request.data['agent_password']:
                bookobj.partial_payment_allowed = True
                bookobj.partial_allowed_by = agent_obj
                bookobj.save()
                return Response({"message":"You sucessfully allow partial payment for this order."},status=status.HTTP_200_OK)
                # return Response({"message":"You enter wrong user password"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"Order does not exist"},status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"Agent doest not exists"},status=status.HTTP_404_NOT_FOUND)




{
    "jTracker_id" : "J123",
    "follow_up_by" : "umer33",
    "dispatch_by" : "",
    "dispatch_fee" : "123",
    "trucker_no" : "",
    "trucker_name" : "",
    "trucker_license" : "",
    "payment_method" : "Credit",
    "payment_status" :False
}
# booking_status = models.CharField(max_length=100,default='Booked')







class JSaveBooking(APIView):
    def post(self,request):
        if not JTrackerConfirmBook.objects.filter(jTracker_id=request.data['jTracker_id']).exists():
            if request.data['follow_up_by'] != '':
                if User.objects.filter(id=request.data['follow_up_by']).exists():
                    data1 = User.objects.get(id=request.data['follow_up_by'])
                    request.data['follow_up_by'] =data1.id
                    print(request.data['follow_up_by'])
                    if request.data['dispatch_by'] != '':
                        if User.objects.filter(id=request.data['dispatch_by']).exists():
                           data2 = User.objects.get(id=request.data['dispatch_by'])
                           request.data['dispatch_by'] = data2.id
                    print("before serail")
                    serail_obj = JTrackSerializer(data=request.data)
                    if serail_obj.is_valid():
                        serail_obj.save()
                        return Response(serail_obj.data,status=status.HTTP_201_CREATED)
                    return Response({"message":serail_obj.errors},status=status.HTTP_400_BAD_REQUEST)
                return Response({"message":"User id does not exists"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"Follow up must required"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Jtracker Id already exists"},status=status.HTTP_400_BAD_REQUEST)
                    # JTrackerConfirmBook



class GetJtrackerBookings(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0
        print(start)
        print(offsetlimit)
        user_obj = UserRole.objects.get(user_id__id=request.user.id)
        if user_obj.role=='A':
            total_items = JTrackerConfirmBook.objects.filter(dispatch_by__id=request.user.id).count()
            bookoing_obj = JTrackerConfirmBook.objects.filter(dispatch_by__id=request.user.id).order_by('-id')[start:offsetlimit]
        else:
            total_items = JTrackerConfirmBook.objects.all().count()
            bookoing_obj = JTrackerConfirmBook.objects.all().order_by('-id')[start:offsetlimit]
        serail_obj = JTrackSerializer1(bookoing_obj, many=True)
        result = {
            "total_items": total_items,
            "results": serail_obj.data
        }


        return Response(result, status=status.HTTP_200_OK)




{
    "name": "M Umer",
    "image" : "abc132"
}
@permission_classes((permissions.AllowAny,))
class SaveAgreement(APIView):
    def post(self,request):
        Agreement.objects.create(
            full_name=request.data['name'],
            image = request.data['image']

        )
        # lqt = int(request.data['order_id'].strip('LQT'))
        # lqt = lqt - 1000
        # if Leads.objects.filter(id=lqt).exists():
        #     lead_obj = Leads.objects.get(id=lqt)
        #     lead_obj.accept_agreemnt = True
        #     lead_obj.save()
        return Response({"message":"Data Saved succesfully"},status=status.HTTP_201_CREATED)
@permission_classes((permissions.AllowAny,))
class SaveRefundAgreement(APIView):
    def post(self,request):
        RefundAgreement.objects.create(
            full_name=request.data['name'],
            image = request.data['image'],
            amount=request.data['amount'],
            order_id=request.data['order_id'],
            date_of_customer=request.data['date_of_customer'],
        )
        # lqt = int(request.data['order_id'].strip('LQT'))
        # lqt = lqt - 1000
        # if Leads.objects.filter(id=lqt).exists():
        #     lead_obj = Leads.objects.get(id=lqt)
        #     lead_obj.accept_agreemnt = True
        #     lead_obj.save()
        return Response({"message":"Data Saved succesfully"},status=status.HTTP_201_CREATED)

{
    "carrier_name" : "samrock",
    "month": "January",
    "day" : 12,
    "mc_number" : "123df",
    "image": "asfsfsdfsdfsd"
}


@permission_classes((permissions.AllowAny,))
class SaveCarrierAgreeent(APIView):
    def post(self,request):
        CarrierAgreement.objects.create(
            carrier_name=request.data['carrier_name'],
            month = request.data['month'],
            day = request.data['day'],
            mc_number= request.data['mc_number'],
            image = request.data['image'],

        )
        return Response({"message":"Data Saved succesfully"},status=status.HTTP_201_CREATED)



class GetCarrierAgreements(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0
        print(start)
        print(offsetlimit)
        total_items = CarrierAgreement.objects.all().count()
        bookoing_obj = CarrierAgreement.objects.all().order_by('-id')[start:offsetlimit]
        serail_obj = CarrierAgreementSerailizer(bookoing_obj, many=True)
        result = {
            "total_items": total_items,
            "results": serail_obj.data
        }
        # print(serail_obj.data)

        return Response(result, status=status.HTTP_200_OK)




class GetAgreements(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0

        total_items = Agreement.objects.all().count()
        bookoing_obj = Agreement.objects.all().order_by('-id')[start:offsetlimit]
        serail_obj = AgreementSerailizer(bookoing_obj, many=True)
        result = {
            "total_items": total_items,
            "results": serail_obj.data
        }
        # print(serail_obj.data)

        return Response(result, status=status.HTTP_200_OK)

class GetRefundAgreements(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0

        total_items = RefundAgreement.objects.all().count()
        bookoing_obj = RefundAgreement.objects.all().order_by('-id')[start:offsetlimit]
        serail_obj = RefundAgreementSerailizer(bookoing_obj, many=True)
        result = {
            "total_items": total_items,
            "results": serail_obj.data
        }
        # print(serail_obj.data)

        return Response(result, status=status.HTTP_200_OK)


{
"stringtext" : "First Name: john Email: johnctas1@gmail.com Phone: (770) 873-6338  From Zip: 28203 From City: Charlotte From State: NC To Zip: 30121 To City: Cartersville To State: GA Make: Hyundai Model: Elantra Model Year: 2010 Vehicle 1 Type: Car Ship Date: 11/24/2021 Transport Type: Open Vehicle Condition: Not Running"
}
{
    "stringtext" :"First Name: Celtina Reinert Email: Celtina.reinert@gmail.com Phone: (816) 456-2602 From Zip: 65340 From City: Marshall From State: MO To Zip: 70755 To City: Livonia To State: LA Make: Jeep Model: Wrangler Model Year: 2008 Vehicle 1 Type: SUV Ship Date: 01/05/2022 Transport Type: Open Vehicle Condition: Running"
}
class SaveTextLeads(APIView):
    def post(self,request):
        stringtxt=request.data['stringtext']
        if 'first_name' in stringtxt:
            try:

                secnario2 = stringtxt
                full_name = secnario2.split('phone:')[0].replace("first_name:", "").replace("last_name:", "").strip()
                print(full_name)
                phone = secnario2.split('email:')[0].split(':')[-1].strip()
                print(phone)
                email = secnario2.split('pickup_city:')[0].split(':')[-1].strip()
                print(email)
                fromCity = secnario2.split('pickup_state_code:')[0].split(':')[-1].strip()
                print(fromCity)
                fromState = secnario2.split('pickup_zip:')[0].split(':')[-1].strip()
                print(fromState)
                fromZip = secnario2.split('dropoff_city:')[0].split(':')[-1].strip()
                print(fromZip)
                toCity = secnario2.split('dropoff_state_code:')[0].split(':')[-1].strip()
                print(toCity)
                toState = secnario2.split('dropoff_zip:')[0].split(':')[-1].strip()
                print(toState)
                toZip = secnario2.split('estimated_ship_date:')[0].split(':')[-1].strip()
                print(toZip)
                shipDate = secnario2.split('vehicle_runs:')[0].split(':')[-1].strip()
                print(shipDate)
                vehicleRuns = secnario2.split('ship_via_id:')[0].split(':')[-1].strip()
                print(vehicleRuns)
                transportType = secnario2.split('year1:')[0].split(':')[-1].strip()
                print(transportType)
                modelYear = secnario2.split('make1:')[0].split(':')[-1].strip()
                maker = secnario2.split('model1:')[0].split(':')[-1].strip()
                model = secnario2.split('vehicle_type_id1:')[0].split(':')[-1].strip()
                vehicleType = secnario2.split('vehicle_type_id1:')[1].strip()
                leadobj = Leads.objects.create(
                full_name = full_name,
                email = email,
                phone = phone,
                origin_city = fromCity,
                origin_state = fromState,
                origin_zip = fromZip,
                destination_city = toCity,
                destination_state = toState,
                destination_zip = toZip,
                car_maker = maker,
                car_model = model,
                model_year1 = modelYear,
                body_type = vehicleType,
                ship_date1 = shipDate,
                vehilce_run1 = vehicleRuns,
                transport_type1 = transportType
                )
                leadobj.payment_id = 'LQT' +str(1000 + leadobj.id)
                leadobj.save()
                return Response({"message": "Data Saved"},status=status.HTTP_201_CREATED)
            except:
                return Response({"message":"Unable to save data"},status=status.HTTP_400_BAD_REQUEST)



        else:
            try:
                scenario1 = stringtxt
                first_name = scenario1.split('Email:')[0].split(':')[1]

                Email = scenario1.split('Phone:')[0].split(':')[-1]

                phone = scenario1.split('From Zip:')[0].split(':')[-1]

                fromzip = scenario1.split('From City:')[0].split(':')[-1]

                fromCity = scenario1.split('From State:')[0].split(':')[-1]

                fromState = scenario1.split('To Zip:')[0].split(':')[-1]

                toZip = scenario1.split('To City:')[0].split(':')[-1]

                toCity = scenario1.split('To State:')[0].split(':')[-1]

                toState = scenario1.split('Make:')[0].split(':')[-1]

                carmaker = scenario1.split('Model:')[0].split(':')[-1]

                carModel = scenario1.split('Model Year:')[0].split(':')[-1]

                modelYear = scenario1.split('Vehicle 1 Type:')[0].split(':')[-1]

                vechleType = scenario1.split('Ship Date:')[0].split(':')[-1]

                ShipDate = scenario1.split('Transport Type:')[0].split(':')[-1]

                tansportType = scenario1.split('Vehicle Condition:')[0].split(':')[-1]

                vechileCondition = scenario1.split('Vehicle Condition:')[1]

                leadobj = Leads.objects.create(
                    full_name=first_name,
                    email=Email,
                    phone=phone,
                    origin_city=fromCity,
                    origin_state=fromState,
                    origin_zip=fromzip,
                    destination_city=toCity,
                    destination_state=toState,
                    destination_zip=toZip,
                    car_maker=carmaker,
                    car_model=carModel,
                    model_year1=modelYear,
                    body_type=vechleType,
                    ship_date1=ShipDate,
                    vehilce_run1=vechileCondition,
                    transport_type1=tansportType
                )
                leadobj.payment_id = 'LQT' + '1000' + str(leadobj.id)
                leadobj.save()
                return Response({"message":"Data saved"}, status=status.HTTP_201_CREATED)
            except Exception as e:

                if 'duplicate key value violates' in str(e):
                    return Response({"message":"Record already exists"},status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Unable to save data"}, status=status.HTTP_400_BAD_REQUEST)



data1= {"first_name" : "Umer Zafar",
        "Email" : "abc@gmail.com",
        "phone" : 4504554,
        "fromCity" : "Plano",
        "fromState" : "TX",
        "fromzip" : "75023",
        "toCity"  : "Washington",
        "toState" : "WS" ,
        "toZip"   : "10012" ,
        "carmaker" : "Honda" ,
        "carModel" : "City" ,
        "modelYear" :"2020",
        "vechleType": "SUV",
        "ShipDate" : "10/12/21",
        "vechileCondition" : "Running",
        "tansportType" : "Open",
        "price" : 1100,
        "is_paid" : False,
        "is_operable" : "Operable",
        "called_by" : "Zyan",
        "received_by": "abc.com",
        "internal_notes" : "not picking up call"
}



class UpdateLeads(APIView):
    def put(self,request,lead_id):
        if Leads.objects.filter(id=lead_id).exists():
            lead_obj = Leads.objects.get(id=lead_id)
            lead_obj.full_name = request.data['first_name']
            lead_obj.email = request.data['Email']
            lead_obj.phone = request.data['phone']
            lead_obj.origin_city = request.data['fromCity']
            lead_obj.origin_state = request.data['fromState']
            lead_obj.origin_zip = request.data['fromzip']
            lead_obj.destination_city = request.data['toCity']
            lead_obj.destination_state = request.data['toState']
            lead_obj.destination_zip = request.data['toZip']
            lead_obj.car_maker = request.data['carmaker']
            lead_obj.car_model = request.data['carModel']
            lead_obj.model_year1 = request.data['modelYear']
            lead_obj.body_type = request.data['vechleType']
            lead_obj.ship_date1 = request.data['ShipDate']
            lead_obj.vehilce_run1 = request.data['vechileCondition']
            lead_obj.transport_type1 = request.data['tansportType']
            lead_obj.price = request.data['price']
            lead_obj.is_paid = request.data['is_paid']
            lead_obj.is_operable = request.data['is_operable']
            lead_obj.called_agent_name = request.data['called_by']
            # lead_obj.received_date = request.data['received_date']
            lead_obj.received_by = request.data['received_by']
            lead_obj.internal_notes =  request.data['internal_notes']
            lead_obj.is_ok = request.data['is_ok']
            lead_obj.save()

            return Response({"message":"Data updated sucessfully"},status=status.HTTP_200_OK)
        return Response({"message":"Data not exists"},status=status.HTTP_400_BAD_REQUEST)

# @permission_classes((permissions.AllowAny,))


class GenerateInvoice(APIView):
    def put(self,request,lead_id):
        if Leads.objects.filter(id=lead_id).exists():
            lead_obj = Leads.objects.get(id=lead_id)
            lead_obj.first_payment = request.data['first_payment']
            lead_obj.first_payment_due = request.data['first_payment_due']
            lead_obj.next_payment = request.data['next_payment']
            lead_obj.next_payment_due = request.data['next_payment_due']
            lead_obj.next_payment_due = request.data['next_payment_due']
            lead_obj.next_payment_due = request.data['accept_agreemnt']
            lead_obj.save()

            return Response({"message":"Data updated sucessfully"},status=status.HTTP_200_OK)
        return Response({"message":"Data not exists"},status=status.HTTP_400_BAD_REQUEST)


class DeleteLead(APIView):
    def delete(self,request,lead_id):
        if Leads.objects.filter(id=lead_id).exists():
            Leads.objects.filter(id=lead_id).delete()
            return Response({"message":"Sucessfully deleted"},status=status.HTTP_202_ACCEPTED)
        return Response({"message":"Lead does not exists"})

# @permission_classes((permissions.AllowAny,))

class DetailLead(APIView):
    def get(self,request,lead_id):
        lqt=int(lead_id.strip('LQT'))
        lqt=lqt-1000
        print('print',lqt)
        if Leads.objects.filter(id=lqt).exists():

            lead_obj = Leads.objects.get(id=lqt)
            print('nice',lead_obj.full_name)
            dic = {

            "id" : lqt,
            "full_name" : lead_obj.full_name,
            "email" :lead_obj.email,
            "phone" : lead_obj.phone,
            "origin_address" :lead_obj.origin_address ,
            "origin_city" : lead_obj.origin_city,
            "origin_state" : lead_obj.origin_state,
            "origin_zip" : lead_obj.origin_zip,
            "destination_address" : lead_obj.destination_address,
            "destination_city" : lead_obj.destination_city,
            "destination_state" : lead_obj.destination_state,
            "destination_zip" : lead_obj.destination_zip,
            "car_maker": lead_obj.car_maker,
            "car_model": lead_obj.car_model,
            "body_type": lead_obj.body_type,
            "model_year": lead_obj.model_year1,
            "ship_date": lead_obj.ship_date1,
            "transport_type": lead_obj.transport_type1,
            "vehilce_run": lead_obj.vehilce_run1,
            "called_agent_name": lead_obj.called_agent_name,
            "is_operable": lead_obj.is_operable,
            "is_paid": lead_obj.is_operable,
            "price": lead_obj.price,
            "received_by": lead_obj.received_by,
            "received_date": lead_obj.received_date,
            "model_year1": lead_obj.model_year1,
            "ship_date1": lead_obj.ship_date1,
            "transport_type1": lead_obj.transport_type1,
            "vehilce_run1": lead_obj.vehilce_run1,
            "internal_notes": lead_obj.internal_notes,
            "is_ok": lead_obj.is_ok,
            "payment_id": lead_obj.payment_id,
            "payment_date": lead_obj.payment_date,
            "assigend_to": lead_obj.assigned_to_id,
            "lead_status": lead_obj.lead_status,
            "third_party": lead_obj.third_party,
            "dispatched_by": lead_obj.dispatched_by,
            "payment_channel": lead_obj.payment_channel,
            "trucker_license": lead_obj.trucker_license,
            "trucker_name": lead_obj.trucker_name,
            "trucker_no": lead_obj.trucker_no,
            "email_count": lead_obj.email_count,
            "agent_price": lead_obj.agent_price,
            "payment_response": lead_obj.payment_response,
            'accept_agreemnt': lead_obj.accept_agreemnt,
            'first_payment': lead_obj.first_payment,
            'first_payment_due': lead_obj.first_payment_due,
            'next_payment': lead_obj.next_payment,
            'next_payment_due': lead_obj.next_payment_due

            }
            result = {
                "total_items": 1,
                "data": dic
            }
            print(result)
            print('ho ha')
            return Response(result, status=status.HTTP_200_OK)


class GetUserRole(APIView):
    def get(self,request):
        try:
            roleobj = UserRole.objects.get(user_id_id=request.user.id)
            user_obj= User.objects.get(id=request.user.id)
            return Response({"message":roleobj.role,"email":user_obj.email,"username":user_obj.username,"phone_no":user_obj.last_name,"full_name": user_obj.first_name},status=status.HTTP_200_OK)
        except:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)



# class GetUserEmail(APIView):
#     def get(self,request):



{
    "lead_id" : 77,
    "assigned_to" : 2
}

class AssignedtoAgent(APIView):
    def put(self,request):
        try:
            lead_obj = Leads.objects.get(id=request.data['lead_id'])

            # if lead_obj.assigned_to==None:
            user_obj = User.objects.get(id=request.data['assigned_to'])
            lead_obj.assigned_to = user_obj
            lead_obj.lead_status = None
            lead_obj.save()
            lead_data=LeadsSerializer(lead_obj)
            emailsending_agent.after_response(lead_data.data,'request_booking_agent.html',
                                              'Quantum Transport Lead Notification',user_obj)
            return Response({"message":"Lead Successfully assigned to Agent"},status=status.HTTP_200_OK)
            # return Response({"message":"Lead Already Assigned"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":"Lead Not found"},status=status.HTTP_404_NOT_FOUND)

{
    "lead_ids" : [177,172],
    "assigned_to" : 2
}
class BulkAssingtoAgent(APIView):
    def put(self,request):
        try:
            user_obj = User.objects.get(id=request.data['assigned_to'])
            lead_data = Leads.objects.filter(id__in=request.data['lead_ids'])
            leads_id = lead_data.values_list('payment_id',flat=True)
            lead_data=lead_data.update(assigned_to=user_obj,lead_status=None)

            bulk_assing_email.after_response(leads_id, 'bulk_assing_email.html',
                                              'Quantum Transport Lead Notification', user_obj)
            return Response({"message":"Leads successfully assigned to Agent"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"User does not exists"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        Leads.objects.filter(id__in=request.data['lead_ids']).delete()
        return Response({"message":"Leads deleted successfully"},status=status.HTTP_202_ACCEPTED)










class GetSpecificAgentLeads(APIView):
    def get(self,request,status_new):
        q1 = Q()
        if status_new=='Leads':
            status_new=None
            q1 |= Q(lead_status=None)
            q1 |= Q(lead_status="")
        else:
            q1 &= Q(lead_status=status_new)
        q1 &= Q(assigned_to__id=request.user.id)


        # if status_new==None:
        lead_obj = Leads.objects.filter(q1).order_by('-id')
        # else:
            # lead_obj = Leads.objects.filter(assigned_to__id=request.user.id, lead_status=status_new).order_by('-id')
        serial_obj = LeadsSerializer(lead_obj,many=True)
        return Response(serial_obj.data,status=status.HTTP_200_OK)


{
    "lead_id" : 77,
    "lead_status" : "Quote"
}

class UpdateLeadStatus(APIView):
    def put(self,request):
        try:
            lead_obj = Leads.objects.get(id=request.data['lead_id'])
            if request.data['lead_status']=="":
                lead_status1 = None
            else:
                lead_status1 = request.data['lead_status']
            lead_obj.lead_status = lead_status1
            lead_obj.save()
            return Response({"mesasge":"Lead Stauts Updated"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"Lead does not exists"},status=status.HTTP_404_NOT_FOUND)






{
 "full_name" : "Sam Rock",
    "email"  :"sam@outlook.com",
    "phone" : "3242324",
    "origin_city" : "Plano",
    "origin_state" : "Texas" ,
    "origin_zip" : "750223",
    "destination_city" : "New York",
    "destination_state" : "New York",
    "destination_zip" : "32422",
    "car_maker" : "Toyota",
    "car_model" : "Yaris",
    "model_year1" :"2020",
    "body_type" : "SUV",
    "ship_date1" :"12/23/2021",
    "vehilce_run1" : "Yes",
    "transport_type1" : "Open",
    "price" : 730,
    "received_by" : "abc.com"
}

@permission_classes((permissions.AllowAny,))
class InsertLeads(APIView):
    def post(self,request):
        if not Leads.objects.filter(origin_zip=request.data['origin_zip'],destination_zip=request.data['destination_zip'],car_maker=request.data['car_maker'],car_model=request.data['car_model']).exists():
            serizl_obj = LeadsSerializer1(data=request.data)

            request.data['third_party'] = True
            if request.data['received_by'] == 'Ibility':
                request.data['received_by'] = 'Cherry'
            elif request.data['received_by'] == 'LeadFI':
                request.data['received_by'] = 'Mango'
            elif request.data['received_by'] == 'TOLM':
                request.data['received_by'] = 'Banana'
            elif request.data['received_by'] == 'cartransportleads':
                request.data['received_by'] = 'Orange'
            elif request.data['received_by'] == 'LeadDrive':
                request.data['received_by'] = 'Melon'
            elif request.data['received_by'] == 'AutoTransportLead':
                request.data['received_by'] = 'Peach'
            else:
                request.data['received_by'] = 'New'



            if serizl_obj.is_valid():
                resp = serizl_obj.save()
                resp.payment_id = 'LQT' +str(1000 + resp.id)
                resp.save()


                emailsending_admin.after_response(request.data, 'request_booking.html', 'Quantum Transport Lead Notification')
                return Response({"message":"Data Inserted Successfully"},status=status.HTTP_201_CREATED)
            return Response(serizl_obj.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Data already exists"},status=status.HTTP_400_BAD_REQUEST)





{
    "id" : "LQT1000118",
    "user_id" :1,
    "price" : 1233,
    "trucker_name" : "sam",
    "trucker_license" : "avc123",
    "trucker_no" : "asda123",
    "payment_type" : "COD"
}

class ConfirmLeads(APIView):
    def post(self,request):
        if Leads.objects.filter(payment_id=request.data['id']).exists():
            if User.objects.filter(id=request.data['user_id']).exists():
                user_obj = User.objects.get(id=request.data['user_id'])
                lead_obj = Leads.objects.get(payment_id=request.data['id'])
                lead_obj.agent_price = request.data['price']
                lead_obj.trucker_name = request.data['trucker_name']
                lead_obj.trucker_license = request.data['trucker_license']
                lead_obj.trucker_no = request.data['trucker_no']
                lead_obj.payment_channel = request.data['payment_type']
                lead_obj.dispatched_by = user_obj
                lead_obj.save()
                return Response({"message":"Leads successfully confirmed"},status=status.HTTP_200_OK)
            return Response({"message":"User does not exists"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Lead does not exists"},status=status.HTTP_400_BAD_REQUEST)

import phonenumbers
from phonenumbers import NumberParseException

@permission_classes((permissions.AllowAny,))

class PhoneVerification(APIView):
    def post(self,request):
        try:
            phone=request.data['phone']
            # try:
            #     phone_number = phonenumbers.parse(phone, None)
            #     if not phonenumbers.is_valid_number(phone_number):
            #         print('hello')
            #         # self.add_error('phone_number', 'Invalid phone number')
            # except NumberParseException as e:
            #     print(e)

            verification = twilio_client.verifications(phone, 'sms')
                    # return redirect('token_validation')
            return Response({"message":"SMS Sent"},status=status.HTTP_200_OK)
        except:
            return Response({"message": "Something Wrong Try Again"}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.AllowAny,))
class EnterCode(APIView):
    def post(self,request):
        try:
            phone=request.data['phone']
            phone_token = request.data['token']
            verification = twilio_client.verification_checks(phone,phone_token)
            print('code is', verification.status)

            if verification.status == 'approved':
                return Response({"message":"Code Verified"},status=status.HTTP_200_OK)
            else:
                return Response({"message": "Enter Valid Code"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something Wrong Try Again"}, status=status.HTTP_400_BAD_REQUEST)
        # try:
        #     phone_number = phonenumbers.parse(phone, None)
        #     if not phonenumbers.is_valid_number(phone_number):
        #         print('hello')
        #         # self.add_error('phone_number', 'Invalid phone number')
        # except NumberParseException as e:
        #     print(e)

        # verification = twilio_client.verifications(phone, 'sms')
        #         # return redirect('token_validation')
        # return Response({"message":"SMS Sent"},status=status.HTTP_400_BAD_REQUEST)
@permission_classes((permissions.AllowAny,))
class SortAgents(APIView):
    def get(self,request,key):
        try:
            print('key is ',key)
            if key == 'empty':
                print('not')
                user_obj = User.objects.filter(samrock__role='A').order_by('username')
                serial_obj = UserSerializer(user_obj, many=True)
                return Response(serial_obj.data, status=status.HTTP_200_OK)
            else:
                user_obj = User.objects.filter(samrock__role='A',username__icontains=key).order_by('username')
                # user_obj = User.objects.filter(samrock__role='A')
                serial_obj = UserSerializer(user_obj, many=True)

        except:
            print('mango')
            user_obj = User.objects.filter(samrock__role='A').order_by('username')
            serial_obj = UserSerializer(user_obj, many=True)
        return Response(serial_obj.data, status=status.HTTP_200_OK)
        # data1 = UserSerializer(user_obj)
        # return Response(data1.data,status=status.HTTP_200_OK)


{
    "year" : "",
    "make": "",
    "model" : "",
    "price" : "",
    "name": "",
    "from_city": "",
    "from_state": "",
    "to_city": "",
    "to_state": "",
    "username": "",
    "user_email": "",
    "user_phone": "",
}
{
    "lead_id": 1782,
    "template_name": "justspoke",
    "subject": "This is subject"
}

class EmailsSend(APIView):
    def post(self,request):
        user_obj = User.objects.get(id=request.user.id)
        if Leads.objects.filter(id=request.data['lead_id']).exists():
            lead_obj = Leads.objects.get(id=request.data['lead_id'])
            if lead_obj.price > 5:
                if lead_obj.email_count==None or lead_obj.email_count=="":
                    previous_email = 0
                else:
                    previous_email = lead_obj.email_count

                try:
                    lead_obj.email_count = previous_email + 1
                except:
                    pass

                lead_obj.save()
                template_name = None
                if request.data["template_name"]=='newquote':
                    template_name = '{0}_NewQuote.html'.format(request.data["company_name"])
                elif request.data["template_name"]== 'voicemail':
                    template_name = '{0}_VoiceMail.html'.format(request.data["company_name"])
                elif request.data['template_name']== 'justspoke':
                    template_name= '{0}_justspoke.html'.format(request.data["company_name"])
                lead_serail = LeadsSerializer1(lead_obj)
                emailsending_users.after_response(lead_serail.data,template_name,request.data['subject'],user_obj.email,user_obj,request.data["from"])

                return Response({"message":"Email Send"},status=status.HTTP_200_OK)
            return Response({"message":"Price is required for Email sending."},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Lead does not exists"},status=status.HTTP_400_BAD_REQUEST)




class getConfirmLeads(APIView):
    def get(self,request,page_no):
        if page_no:
            offsetlimit = page_no * 10
            start = offsetlimit - 10
        else:
            offsetlimit = 10
            start = 0
        user_role = UserRole.objects.get(user_id__id=request.user.id)
        if user_role.role =='A':
            total_obj = Leads.objects.filter(dispatched_by__id=request.user.id).count()
            lead_obj = Leads.objects.filter(dispatched_by__id=request.user.id).order_by('-id')[start:offsetlimit]
        else:
            total_obj = Leads.objects.exclude(dispatched_by=None).count()
            lead_obj = Leads.objects.exclude(dispatched_by=None).order_by('-id')[start:offsetlimit]
        # else:
        # lead_obj = Leads.objects.filter(assigned_to__id=request.user.id, lead_status=status_new).order_by('-id')
        serial_obj = LeadsSerializer(lead_obj, many=True)
        data = {
            "total_record" : total_obj,
            "data" : serial_obj.data
        }
        return Response(data, status=status.HTTP_200_OK)


{
    "lead_status" : None,
    "lead_id": None,
    "assigend_status" : None,
    "is_ok" : True,
    "assigned_to" :None,
    "received_from" : "Ibility",
    "start_date" : "2022-01-26",
    "end_date": "2022-01-26",
    "full_name" : "matt"
}
# @permission_classes((permissions.AllowAny,))
class testSearch(APIView):
    def post(self,request,page_no):

        if page_no:
            limit = 50
            offsetlimit = page_no * 50
            start = offsetlimit - 50
        else:
            limit = 50
            # offsetlimit = 50
            start = 0

        data = request.data['full_name']
        ls = ''
        # request.user.id=5
        user_obj = UserRole.objects.get(user_id__id=request.user.id)
        # user_obj = UserRole.objects.get(user_id__id=5)
        if user_obj.role=='S':
            lead_status = request.data['lead_status']
            if lead_status!=None and lead_status!="":
                ls = ls + ' "lead_status"=\'' + str(lead_status) + '\''
        elif user_obj.role =='A':
            lead_status = request.data['lead_status']
            if lead_status!=None and lead_status!='Leads':
                ls = ls + ' "lead_status"=\'' + str(lead_status) + '\''
            elif lead_status=="Leads":
                ls = ls + ' "lead_status" is NULL '
            else:
                pass
            if ls == '':
                ls = ls + ' "assigned_to_id"=\'' + str(request.user.id) + '\''
            else:
                ls = ls + 'And "assigned_to_id"=\'' + str(request.user.id) + '\''
        if 'lead_id' in request.data.keys():
            if request.data['lead_id'] != None and request.data['lead_id'] != "":
                if ls == '':
                    ls = ls + ' "payment_id"=\'' + str(request.data['lead_id']) + '\''
                else:
                    ls = ls + 'And "payment_id"=\'' + str(request.data['lead_id']) + '\''

        if 'assigend_status' in request.data.keys():
            if request.data['assigend_status']!=None and request.data['assigend_status']!="":
                if request.data['assigend_status']=='Unassigned':
                    if ls!='':
                        ls = ls + 'And "assigned_to_id" is NULL '
                    else:

                        ls = ls + ' "assigned_to_id" is NULL '
                    # q1 &= Q(assigned_to=None)
                if request.data['assigend_status']=='Assigned':
                    if ls!='':
                        ls = ls + 'And "assigned_to_id" is not NULL '
                    else:

                        ls = ls + ' "assigned_to_id" is not NULL '
        if request.data['is_ok'] != None and request.data['is_ok']!="":
            if ls == '':
                ls = ls + ' "is_ok"=\'' + str(request.data['is_ok']) + '\''
            else:
                ls = ls + 'And "is_ok"=\'' + str(request.data['is_ok']) + '\''
        if request.data['assigned_to'] !=None and request.data['assigned_to']!="":
            if ls == '':
                ls = ls + ' "assigned_to_id"=\'' + str(request.data['assigned_to']) + '\''
            else:
                ls = ls + 'And "assigned_to_id"=\'' + str(request.data['assigned_to']) + '\''
        if request.data['received_from'] != None and request.data['received_from']!="":
            if ls == '':
                ls = ls + ' "received_by" like\'' + str(request.data['received_from']) + '%\''
            else:
                ls = ls + 'And "received_by" like\'' + str(request.data['received_from']) + '%\''
        if request.data['start_date'] != None and request.data['start_date'] != "":
            # q1 &= Q(received_date__date__gte=request.data['start_date'])
            if ls == '':
                ls = ls + ' "received_date" >=\'' + str(request.data['start_date']) + '\''
            else:
                ls = ls + 'And "received_date" >=\'' + str(request.data['start_date']) + '\''
        if request.data['end_date'] != None and request.data['end_date'] != "":
            # q1 &= Q(received_date__date__gte=request.data['start_date'])
            if ls == '':
                ls = ls + ' "received_date" <=\'' + str(request.data['end_date']) + '\''
            else:
                ls = ls + 'And "received_date" <=\'' + str(request.data['end_date']) + ' 23:59:59\''

        if ls!='' and data!=None and data!='':

            query = 'select * from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')' + 'And' + str(ls)  + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start) ;
            totalitems = 'select count(*) from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')' + 'And' + str(ls) ;

        elif ls=='' and data!=None and data!='':

            query = 'select * from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')' + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start) ;
            totalitems = 'select count(*) from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')'  ;
        elif ls!='' and data==None and data!='':

            query = 'select * from public."booking_leads" where '+str(ls)  + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start);
            totalitems = 'select count(*) from public."booking_leads" where '+str(ls)  ;

        else :
            print('Bhai')
            query = "select * from public.booking_leads where ship_date1 like '%03/%/2023'";
            # query = 'select * from public."booking_leads"'  + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start);
            totalitems = 'select count (*) from public."booking_leads"';
        with connection.cursor() as cursor:
            cursor.execute(query)
            it = cursor.fetchall()
        with connection.cursor() as cur:
            cur.execute(totalitems)
            totalitem = cur.fetchall()
        for i in totalitem:
            total_items = i[0]
        li=[]

        for val in it:
            dic = {
            "id" : val[0],
            "full_name" : val[1],
            "email" : val[2],
            "phone" : val[3],
            "origin_address" : val[4],
            "origin_city" : val[5],
            "origin_state" : val[6],
            "origin_zip" : val[7],
            "destination_address" : val[8],
            "destination_city" : val[9],
            "destination_state" : val[10],
            "destination_zip" : val[11],
            "car_maker" : val[12],
            "car_model" : val[13],
            "body_type" : val[14],
            "model_year" : val[15],
            "ship_date" : val[16],
            "transport_type" : val[17],
            "vehilce_run" : val[18],
            "called_agent_name" : val[19],
            "is_operable":  val[20],
            "is_paid" : val[21],
            "price" : val[22],
            "received_by" : val[23],
            "received_date" : val[24],
            "model_year1" : val[25],
            "ship_date1" : val[26],
            "transport_type1" : val[27],
            "vehilce_run1" : val[28],
            "internal_notes" : val[29],
            "is_ok" : val[30],
            "payment_id" : val[31],
            "payment_date" : val[32],
            "assigend_to" : str(val[33]),
            "lead_status" : val[34],
            "third_party" : val[35],
            "dispatched_by" : val[36],
            "payment_channel" : val[37],
            "trucker_license" : val[38],
            "trucker_name" : val[39],
            "trucker_no" : val[40],
                "email_count": val[41],
                "agent_price" : val[42],
                "payment_response": val[44]
                # "accept_agreemnt" : val[45],
                # 'first_payment':val[46],
                # 'first_payment_due': val[47],
                # 'next_payment': val[48],
                # 'next_payment_due': val[49]

            }
            li.append(dic)
            # print('////////////////')
        result={
            "items_return": len(li),
            "total_items": total_items,
            "results": li,

        }

        return Response(result,status=status.HTTP_200_OK)



@permission_classes((permissions.AllowAny,))
class testSearch_new(APIView):
    def post(self,request,page_no):
        print('Hell In')
        if page_no:
            limit = 50
            offsetlimit = page_no * 50
            start = offsetlimit - 50
        else:
            limit = 50
            # offsetlimit = 50
            start = 0

        data = request.data['full_name']
        ls = ''
        # request.user.id=5
        # user_obj = UserRole.objects.get(user_id__id=request.user.id)
        user_obj = UserRole.objects.get(user_id__id=5)
        if user_obj.role=='S':
            lead_status = request.data['lead_status']
            if lead_status!=None and lead_status!="":
                ls = ls + ' "lead_status"=\'' + str(lead_status) + '\''
        elif user_obj.role =='A':
            lead_status = request.data['lead_status']
            if lead_status!=None and lead_status!='Leads':
                ls = ls + ' "lead_status"=\'' + str(lead_status) + '\''
            elif lead_status=="Leads":
                ls = ls + ' "lead_status" is NULL '
            else:
                pass
            if ls == '':
                ls = ls + ' "assigned_to_id"=\'' + str(request.user.id) + '\''
            else:
                ls = ls + 'And "assigned_to_id"=\'' + str(request.user.id) + '\''
        if 'lead_id' in request.data.keys():
            if request.data['lead_id'] != None and request.data['lead_id'] != "":
                if ls == '':
                    ls = ls + ' "payment_id"=\'' + str(request.data['lead_id']) + '\''
                else:
                    ls = ls + 'And "payment_id"=\'' + str(request.data['lead_id']) + '\''

        if 'assigend_status' in request.data.keys():
            if request.data['assigend_status']!=None and request.data['assigend_status']!="":
                if request.data['assigend_status']=='Unassigned':
                    if ls!='':
                        ls = ls + 'And "assigned_to_id" is NULL '
                    else:

                        ls = ls + ' "assigned_to_id" is NULL '
                    # q1 &= Q(assigned_to=None)
                if request.data['assigend_status']=='Assigned':
                    if ls!='':
                        ls = ls + 'And "assigned_to_id" is not NULL '
                    else:

                        ls = ls + ' "assigned_to_id" is not NULL '
        if request.data['is_ok'] != None and request.data['is_ok']!="":
            if ls == '':
                ls = ls + ' "is_ok"=\'' + str(request.data['is_ok']) + '\''
            else:
                ls = ls + 'And "is_ok"=\'' + str(request.data['is_ok']) + '\''
        if request.data['assigned_to'] !=None and request.data['assigned_to']!="":
            if ls == '':
                ls = ls + ' "assigned_to_id"=\'' + str(request.data['assigned_to']) + '\''
            else:
                ls = ls + 'And "assigned_to_id"=\'' + str(request.data['assigned_to']) + '\''
        if request.data['received_from'] != None and request.data['received_from']!="":
            if ls == '':
                ls = ls + ' "received_by" like\'' + str(request.data['received_from']) + '%\''
            else:
                ls = ls + 'And "received_by" like\'' + str(request.data['received_from']) + '%\''
        if request.data['start_date'] != None and request.data['start_date'] != "":
            # q1 &= Q(received_date__date__gte=request.data['start_date'])
            if ls == '':
                ls = ls + ' "received_date" >=\'' + str(request.data['start_date']) + '\''
            else:
                ls = ls + 'And "received_date" >=\'' + str(request.data['start_date']) + '\''
        if request.data['end_date'] != None and request.data['end_date'] != "":
            # q1 &= Q(received_date__date__gte=request.data['start_date'])
            if ls == '':
                ls = ls + ' "received_date" <=\'' + str(request.data['end_date']) + '\''
            else:
                ls = ls + 'And "received_date" <=\'' + str(request.data['end_date']) + ' 23:59:59\''

        if ls!='' and data!=None and data!='':
            print('query is 1 :',ls)
            query = 'select * from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')' + 'And' + str(ls)  + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start) ;
            totalitems = 'select count(*) from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')' + 'And' + str(ls) ;

        elif ls=='' and data!=None and data!='':
            print('query is 2 :',ls)
            query = 'select * from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')' + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start) ;
            totalitems = 'select count(*) from public."booking_leads" where "tsv_title"@@ plainto_tsquery(\'' + data + '\')'  ;
        elif ls!='' and data==None and data!='':
            print('query is 3 :',ls)
            query = 'select * from public."booking_leads" where '+str(ls)  + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start);
            totalitems = 'select count(*) from public."booking_leads" where '+str(ls)  ;

        else :
            print('query is 4 :',ls)
            ls = '"ship_date1" == 01/02/2013'
            print('Now ls is ',ls)
            # query = 'select * from public."booking_leads"'  + ' order by "id" DESC LIMIT ' + str(limit) + ' OFFSET ' + str(start);

            query = "select * from public.booking_leads where ship_date1 like '%03/%/2023'";
            # query = "select * from public.booking_leads where ship_date1 like '%/2023' and received_by= 'Cherry'";
            # query = "select * from public.booking_leads where ship_date1 like '%/2023' and received_by= 'Cherry'";
            totalitems = 'select count (*) from public."booking_leads"';
        with connection.cursor() as cursor:
            cursor.execute(query)
            it = cursor.fetchall()
        with connection.cursor() as cur:
            cur.execute(totalitems)
            totalitem = cur.fetchall()
        for i in totalitem:
            total_items = i[0]
        li=[]

        for val in it:
            dic = {
            "id" : val[0],
            "full_name" : val[1],
            "email" : val[2],
            "phone" : val[3],
            "origin_address" : val[4],
            "origin_city" : val[5],
            "origin_state" : val[6],
            "origin_zip" : val[7],
            "destination_address" : val[8],
            "destination_city" : val[9],
            "destination_state" : val[10],
            "destination_zip" : val[11],
            "car_maker" : val[12],
            "car_model" : val[13],
            "body_type" : val[14],
            "model_year" : val[15],
            "ship_date" : val[16],
            "transport_type" : val[17],
            "vehilce_run" : val[18],
            "called_agent_name" : val[19],
            "is_operable":  val[20],
            "is_paid" : val[21],
            "price" : val[22],
            "received_by" : val[23],
            "received_date" : val[24],
            "model_year1" : val[25],
            "ship_date1" : val[26],
            "transport_type1" : val[27],
            "vehilce_run1" : val[28],
            "internal_notes" : val[29],
            "is_ok" : val[30],
            "payment_id" : val[31],
            "payment_date" : val[32],
            "assigend_to" : str(val[33]),
            "lead_status" : val[34],
            "third_party" : val[35],
            "dispatched_by" : val[36],
            "payment_channel" : val[37],
            "trucker_license" : val[38],
            "trucker_name" : val[39],
            "trucker_no" : val[40],
                "email_count": val[41],
                "agent_price" : val[42],
                "payment_response": val[44]
                # "accept_agreemnt" : val[45],
                # 'first_payment':val[46],
                # 'first_payment_due': val[47],
                # 'next_payment': val[48],
                # 'next_payment_due': val[49]

            }
            li.append(dic)
            # print('////////////////')
        result={
            "items_return": len(li),
            "total_items": total_items,
            "results": li,

        }

        return Response(result,status=status.HTTP_200_OK)

@permission_classes((permissions.AllowAny,))
class SearchNewLeads(APIView):
    def get(self,request):
        try:

            user_obj = Leads.objects.filter(ship_date1__icontains='2023')
            serial_obj = LeadsSerializer(user_obj, many=True)
            return Response(serial_obj.data, status=status.HTTP_200_OK)

            # user_obj = User.objects.filter(samrock__role='A',username__icontains=key).order_by('username')
            # # user_obj = User.objects.filter(samrock__role='A')
            # serial_obj = UserSerializer(user_obj, many=True)

        except:
            print('mango')
            # user_obj = User.objects.filter(samrock__role='A').order_by('username')
            # serial_obj = UserSerializer(user_obj, many=True)
        return Response(serial_obj.data, status=status.HTTP_200_OK)

class GetAgentDetail(APIView):
    def get(self,request,id):
        user_obj = User.objects.get(id=id)
        data1 = UserSerializer(user_obj)
        return Response(data1.data,status=status.HTTP_200_OK)







@permission_classes((permissions.AllowAny,))
class YearMakeModel(APIView):
    def get(self,request):
        query_set = Leads.objects.all()
        make = query_set.distinct('car_maker').values_list('car_maker',flat=True)
        model = query_set.distinct('car_model').values_list('car_model',flat=True)
        year = query_set.distinct('model_year1').values_list('model_year1',flat=True)
        dic = {
            "make" : make,
            "model" : model,
            "year" : year
        }
        return Response(dic,status=status.HTTP_200_OK)

# class YearMakeModel(mixins.ListModelMixin, generics.GenericAPIView):
#
#
#
#     serializer_class = ModelMakeYearSerializer
#
#     def get_queryset(self):
#         queryset = Leads.objects.all()
#         return queryset
#
#
#     def get(self, request, *args, **kwargs):
#         response = self.list(request, *args, **kwargs)
#         return response
#




class QuickPayment(APIView):
    def post(self,request):
        cvv = request.data['cvv']
        exp_date = request.data['expiry_date']
        amount = request.data['fee']
        e_date = exp_date.split('/')
        month = e_date[0]
        year = e_date[1]
        owner_name = request.data['owner_name']
        creditno = request.data['card_no']
        cardholder_name = request.data['cardholder_name']
        url = 'https://secure.1stpaygateway.net/secure/RestGW/Gateway/Transaction/Sale'
        # url = 'https://secure.merchantonegateway.com/api/transact.php?username=mfarooq75023&password=brainplow786@lahore&type=sale&ccnumber=' + str(
        #     creditno) + '&ccexp=' + str(exp_date) + '&cvv=' + str(cvv) + '&amount=' + str(
        #     amount) + '&descriptor=Quantum Transport Solution.'

        payload = {
            "merchantKey": "984b2d4d-bbc5-41db-9767-69c61e852f92",
            "processorId": "329513",
            "cardNumber": creditno,
            "cardExpMonth": month,
            "cardExpYear": year,
            "transactionAmount": amount,
            "ownerName": "Tariq Farooq",
            "ownerStreet": "Echo Trl",
            "ownerCity": "Dallas",
            "ownerState": "TX",
            "ownerZip": "75023",
            "cVV": cvv

        }

        r = requests.post(url, data=payload)
        code = r.text
        print("result", r.status_code)
        print("result", r.text)

        response_text = code.split('authCode')

        print("split1", response_text[0])

        if '"authResponse":"APPROVED"' in response_text[0] or 'Approved' in response_text[0]:
            QuickPay.objects.create(
                card_no = creditno,
                card_holder_name = cardholder_name,
                amount = amount,
                lead_id = lead_id

            )
            return Response({"message":"Payment Successfulle"},status=status.HTTP_200_OK)
        elif 'Credit card number entered is not valid' in response_text[1]:
            print("Credit card number wrong")
            return Response({"message": "Invalid Card Number"}, status=status.HTTP_400_BAD_REQUEST)

        elif 'TRANS DENIED DO NOT HONOR' in response_text[1]:
            print("cvv or exp wrong")
            status_text = 'Invalid cvv or exp'
            return Response({"message": "Invalid Cvv or Expiry"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("something went wrong")
            return Response({"message": "Something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)