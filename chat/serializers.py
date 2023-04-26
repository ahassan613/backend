from rest_framework import serializers
from .models import *





class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetail
        fields = '__all__'
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'
        # fields = ('id','user1', 'user2','','')
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
class Post_Msg_Serializer(serializers.ModelSerializer):
    class Meta:
        model= Message
        fields=('SenderIsCustomer','MessageText','Room')


#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','last_login','is_superuser','first_name','last_name','email','is_staff','is_active','date_joined',)
#         # read_only_fields = fields
#
#
# class ConfirmBookingSerail(serializers.ModelSerializer):
#     class Meta:
#         model = ConfirmBook
#         fields = '__all__'
#
#
#
# class BookingSerializer1(serializers.ModelSerializer):
#     # book_detail = ConfirmBookingSerail()
#     # locked_by = AgentSerializer()
#     class Meta:
#         model = Booking
#         fields = '__all__'
#
