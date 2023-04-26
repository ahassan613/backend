from rest_framework import serializers
from .models import *

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentDetail
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','last_login','is_superuser','first_name','last_name','email','is_staff','is_active','date_joined',)
        # read_only_fields = fields


class ConfirmBookingSerail(serializers.ModelSerializer):
    class Meta:
        model = ConfirmBook
        fields = '__all__'



class BookingSerializer1(serializers.ModelSerializer):
    # book_detail = ConfirmBookingSerail()
    # locked_by = AgentSerializer()
    class Meta:
        model = Booking
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    book_detail = ConfirmBookingSerail()
    assigned_to = UserSerializer()
    class Meta:
        model = Booking
        fields = '__all__'



class ConatctusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'




class LeadsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self,instance):
        print(instance.assigned_to)
        username= 'umer'
        return username
    # assigned_to = UserSerializer()
    class Meta:
        model = Leads
        fields = '__all__'

class LeadsSerializer1(serializers.ModelSerializer):
    # assigned_to = UserSerializer()
    class Meta:
        model = Leads
        fields = '__all__'


class JTrackSerializer1(serializers.ModelSerializer):
    follow_up_by=UserSerializer()
    dispatch_by=UserSerializer()
    class Meta:
        model = JTrackerConfirmBook
        fields = '__all__'

class JTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = JTrackerConfirmBook
        fields = '__all__'



class AgreementSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = '__all__'

class RefundAgreementSerailizer(serializers.ModelSerializer):
    class Meta:
        model = RefundAgreement
        fields = '__all__'



class CarrierAgreementSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CarrierAgreement
        fields = '__all__'



class roleSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = UserRole
        fields = ('role','id','user_id',)

    # read_only_fields = fields

    # read only fields

    # def get_exercises(self, obj):
    #     qs = obj.exercises.all().order_by('index')
    #     return UserSerializer(qs, many=True, read_only=True).data


# class ModelMakeYearSerializer(serializers.ModelSerializer):
#     years = serializers.SerializerMethodField()
#     make = serializers.SerializerMethodField()
#     model = serializers.SerializerMethodField()
#
#
#     def get_years(self,request):





