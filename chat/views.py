# chat/views.py
from django.shortcuts import render
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
from django.db.models import Q
# Create your views here.
import after_response
from django.template.loader import get_template
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def index(request):
    return render(request, 'chat/index.html')



def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

@permission_classes((permissions.AllowAny,))
class AddRoom(APIView):
    def post(self,request):
        customer_data_seral = CustomerDataSerializer(data=request.data)
        if customer_data_seral.is_valid():
            customer_data_seral.save()
            customer_id=customer_data_seral.data['id']
            print('Customer id is',customer_data_seral.data['id'])
            dic1 = {}
            print(request.data)
            try:
                user_agent = 'umer'
                user2 = User.objects.get(username=user_agent)
                dic1 = {"user1": customer_id, "user2": user2.id}
                serizl_obj = RoomSerializer(data=dic1)
                if serizl_obj.is_valid():
                    resp = serizl_obj.save()
                    resp.save()
                    print('Room id',resp.id)
                    new_dict = dict()
                    new_dict["room"] = resp.id
                    new_dict["messasge"]="Room Created"
                    return Response(new_dict, status=status.HTTP_201_CREATED)
            except Exception as e:
                    print(e)
                    print('something wrong in excepetion')
        return Response(customer_data_seral.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes((permissions.AllowAny,))
class GetAllRooms(APIView):
    def get(self, request, id):

        # agent_name='azhar'
        # user_id = User.objects.get(username=agent_name)
        rooms = Rooms.objects.filter(user2=id)
        total_obj = len(rooms)
        serail_obj = RoomSerializer(rooms, many=True)
        result = {
            "total_items": total_obj,
            "data": serail_obj.data
        }
        return Response(result, status=status.HTTP_200_OK)
    # Room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    # SenderIsCustomer =models.BooleanField(default=None)
    # MessageText = models.CharField(max_length=10000)
    # Seen = models.BooleanField(default=False)
    # Deleted = models.BooleanField(default=False)
    # CreatedAt = models.DateTimeField(auto_now_add=True)

@permission_classes((permissions.AllowAny,))
class GetMessages(APIView):
    def get(self, request, roomid, items):
        new_dict = dict()
        # messages = Message.objects.filter(Room=id).order_by('-CreatedAt')
        # print("messages",messages)
        res = Message.objects.filter(Room=roomid).order_by('-CreatedAt')
        # print('res', res)
        paginator = Paginator(res, items)
        page = request.GET.get('page')
        # print(page)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer1 = MessageSerializer(data, many=True, context=serializer_context)
        items = paginator.count
        pages = paginator.num_pages

        res = {
            'Total Result': items,
            'Total Pages': pages,
            "room_no": roomid,
            'messages': serializer1.data
        }

        return Response(res)

    def post(self, request, roomid,items):
        dic = request.data
        # dic.update({"Sender": request.sender})
        dic.update({"Room": roomid})
        print("Data", dic)
        serializer = Post_Msg_Serializer(data=dic)
        if serializer.is_valid():
            serializer.save()
            messages = Message.objects.filter(Room=roomid).order_by('-CreatedAt')
            paginator = Paginator(messages, items)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            serializer_context = {'request': request}
            serializer1 = MessageSerializer(data, many=True, context=serializer_context)
            items1 = paginator.count
            pages = paginator.num_pages

            res = {
                'Total Result': items1,
                'Total Pages': pages,
                "room_no": roomid,
                'messages': serializer1.data
            }

            return Response(res, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # if page_no:
        #     offsetlimit = page_no * 10
        #     start = offsetlimit - 10
        # else:
        #     offsetlimit = 10
        #     start = 0
        # total_obj = ContactUs.objects.all().count()
        # bookoing_obj = ContactUs.objects.all().order_by('-id')[start:offsetlimit]
        # serail_obj = ConatctusSerializer(bookoing_obj, many=True)
        # result = {
        #     "total_items": total_obj,
        #     "data": serail_obj.data
        # }
        # return Response(result, status=status.HTTP_200_OK)





    # resp.payment_id = 'LQT' + str(1000 + resp.id)
# obj = Rooms(user1=user_customer, user2=user2)
# objr=obj.save()

# @permission_classes((permissions.AllowAny,))
# class GetRoom(APIView):
#     def post(self,request):
#         customer_data_seral = CustomerDataSerializer(data=request.data)
#
#         dic1 = {}
#         user2 = 'umer'
#         try:
#             obj = Rooms.objects.get(id=)
#             # obj = Rooms.objects.get((Q(user1__id=customer_id) & Q(user2__username=user2)) | (
#             #         Q(user1__id=user2) & Q(user2__username=customer_id)))
#             print("in if")
#             if obj:
#                 new_dict = dict()
#
#                 new_dict["room"] = obj.id
#                 new_dict["messasge"] = "Room exist"
#                 return Response(new_dict, status=status.HTTP_302_FOUND)
#
#         except:
#             print('else .....................')
#             print(request.data)
#             user2 = User.objects.get(username=user2)
#             user1 = CustomerDetail.objects.get(id=customer_id)
#             dic1 = {"user1": user1, "user2": user2}
#
#             obj = Rooms(user1=user1, user2=user2)
#             obj.save()
#
#             objr = Rooms.objects.get(user1=user1, user2=user2)
#             if objr:
#                 new_dict = dict()
#
#                 new_dict["room"] = objr.id
#                 new_dict["messasge"]="Data Saved"
#                 return Response(new_dict, status=status.HTTP_201_CREATED)
#
#         return Response(customer_data_seral.errors, status=status.HTTP_400_BAD_REQUEST)



