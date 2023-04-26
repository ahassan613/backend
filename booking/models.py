from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class UserRole(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,related_name='samrock')
    User_choices = (
        ('S', 'Super_Admin'),
        ('A', 'Agent'),
    )
    role = models.CharField(max_length=1, choices=User_choices, blank=True)



class AgentDetail(models.Model):
    agent_name = models.CharField(max_length=30)
    agent_id = models.CharField(max_length=30)
    agent_password = models.CharField(max_length=50,default='bpl321')
    # location=models.CharField(max_length=30)
{
 "full_name" : "Sam Rock",
    "email"  :"sam@outlook.com",
    "phone" : "3242324",
    "origin_city" : "Plano",
    "origin_state" : "Texas" ,
    "origin_zip" : "75023",
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
    "price" : 0,
    "received_by" : "CarTransportLead"
}
class Booking(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    pick_up = models.CharField(max_length=500)
    drop_off = models.CharField(max_length=500)
    pick_up_date = models.DateField()

    book_time = models.DateTimeField(auto_now_add=True)
    # locked = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    vehicle_run = models.BooleanField(default=None)
    type_of_service = models.CharField(max_length=100,default='')

    make = models.CharField(default=None,null=True,max_length=100)
    model = models.CharField(default=None,null=True,max_length=100)
    year = models.CharField(default=None,null=True,max_length=100)


class ConfirmBook(models.Model):
    order_id = models.CharField(max_length=100,null=True)
    booking_id = models.OneToOneField(Booking,on_delete=models.CASCADE,related_name="book_detail")
    booking_fee = models.FloatField()
    fee_status = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)
    payment_response = models.CharField(max_length=3000,null=True,default="")
    truck_name = models.CharField(max_length=100,default=None)
    truck_no = models.CharField(max_length=100,default=None)
    trucker_license = models.CharField(max_length=100,default=None,null=True,blank=True)
    partial_payment_allowed = models.BooleanField(default=False)
    partial_allowed_by = models.ForeignKey(AgentDetail,on_delete=models.CASCADE,null=True,default=None)
    remaning_fee = models.CharField(max_length=100,default=None,null=True,blank=True)



class PartialPayment(models.Model):
    booking_id = models.ForeignKey(ConfirmBook,on_delete=models.CASCADE)
    partial_fee = models.CharField(max_length=100)
    payment_date = models.DateField(auto_now_add=True)
    payment_response = models.CharField(max_length=200,default=None,null=True)
    # actual_payment = models.CharField(max_length=100)

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    locked = models.BooleanField(default=False)
    locked_by = models.ForeignKey(AgentDetail, null=True, on_delete=models.CASCADE)




class Leads(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=200)
    origin_address = models.CharField(max_length=200,null=True,blank=True)
    origin_city = models.CharField(max_length=200)
    origin_state = models.CharField(max_length=200)
    origin_zip = models.CharField(max_length=100)
    destination_address = models.CharField(max_length=200,null=True,blank=True)
    destination_city = models.CharField(max_length=200)
    destination_state = models.CharField(max_length=200)
    destination_zip = models.CharField(max_length=100)
    car_maker = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    model_year1 = models.CharField(max_length=100,default=None,null=True,blank=True)
    body_type = models.CharField(max_length=100,null=True,blank=True)
    ship_date1 = models.CharField(null=True,blank=True,default=None,max_length=100)
    vehilce_run1 = models.CharField(null=True,blank=True,default=None,max_length=20)
    transport_type1 = models.CharField(null=True,blank=True,default=None,max_length=30)
    price = models.FloatField(default=None,null=True,blank=True)
    is_paid = models.BooleanField(default=False)
    called_agent_name = models.CharField(max_length=100,null=True,blank=True,default=None)
    is_operable = models.CharField(max_length=100,null=True,blank=True,default=None)
    received_date = models.DateTimeField(auto_now_add=True,null=True)
    received_by = models.CharField(max_length=100,null=True,blank=True,default=None)
    actual_received_by = models.CharField(max_length=100,null=True,blank=True,default=None)
    internal_notes = models.CharField(max_length=1000,null=True,blank=True,default=None)
    is_ok = models.BooleanField(default=False)
    payment_id = models.CharField(default=None,null=True,blank=True,max_length=200)
    payment_date = models.CharField(default=None,null=True,blank=True,max_length=300)
    payment_response = models.CharField(max_length=10000,null=True,blank=True,default=None)
    agent_price = models.FloatField(default=None,null=True,blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,default=None)
    lead_status = models.CharField(max_length=25,null=True,blank=True,default=None)
    third_party = models.BooleanField(default=False)
    payment_channel = models.CharField(null=True,blank=True,default=None,max_length=200)
    dispatched_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,default=None,related_name='distpatch')
    trucker_name = models.CharField(max_length=200,null=True,blank=True,default=None)
    trucker_no = models.CharField(max_length=200,null=True,blank=True,default=None)
    trucker_license = models.CharField(max_length=200,null=True,blank=True,default=None)
    email_count = models.IntegerField(default=0,null=True,blank=True)
    # message_count = models.IntegerField(default=0,null=True,blank=True)
    # accept_agreemnt = models.BooleanField(default=False)
    # first_payment = models.CharField(max_length=100,null=True,blank=True,default=None)
    # first_payment_due = models.CharField(max_length=300,null=True,blank=True,default=None)
    # next_payment = models.CharField(max_length=100,null=True,blank=True,default=None)
    # next_payment_due = models.CharField(max_length=300,null=True,blank=True,default=None)
    # testing_appp = models.CharField(max_length=300,null=True,blank=True,default=None)






    class Meta:
        unique_together = ('origin_zip','destination_zip','car_maker','car_model')









class JTrackerConfirmBook(models.Model):

    jTracker_id = models.CharField(max_length=150)
    follow_up_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='follower')
    dispatch_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='dispatcher')
    dispatch_fee = models.FloatField()
    trucker_no = models.CharField(max_length=200,null=True,blank=True)
    trucker_name =models.CharField(max_length=200,null=True,blank=True)
    trucker_license = models.CharField(max_length=100,null=True,blank=True)
    payment_method = models.CharField(max_length=200,null=True,blank=True)
    payment_status = models.BooleanField(default=False)
    booking_status = models.CharField(max_length=100,default='Booked')




class Agreement(models.Model):
    full_name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=100000)

class RefundAgreement(models.Model):
    full_name = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=100000)
    amount=models.FloatField(default=None,null=True,blank=True)
    order_id = models.CharField(max_length=100,null=True,blank=True)
    date_of_customer = models.DateTimeField(null=True,blank=True)





class CarrierAgreement(models.Model):
    month = models.CharField(max_length=50)
    day = models.CharField(max_length=50)
    carrier_name = models.CharField(max_length=100)
    mc_number = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    image = models.CharField(max_length=100000)

#
# class CustomerDetail(models.Model):
#     customer_name = models.CharField(max_length=50)
#     customer_phone = models.CharField(max_length=50)
#     customer_email = models.CharField(max_length=100)
#     CreatedAt = models.DateTimeField(auto_now_add=True)



