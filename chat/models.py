from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class Messages(models.Model):
#     room_name = models.CharField(max_length=100)
#     sender = models.CharField(max_length=100)
#     receiver = models.CharField(max_length=100)
#     message = models.CharField(max_length=200)
#     seen = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

class CustomerDetail(models.Model):
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=100)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    # booking_date = models.DateTimeField(auto_now_add=True)

class Dataforchat(models.Model):
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=100)
    # CreatedAt = models.DateTimeField(auto_now_add=True)

class Rooms(models.Model):
    user1 = models.ForeignKey(CustomerDetail, related_name='user1', on_delete=models.CASCADE, default=None)  # customer
    # user1 =models.CharField(max_length=10000)  # post a job
    user2 = models.ForeignKey(User, related_name='user2', on_delete=models.CASCADE, default=None)  # Agent
    Deleted = models.BooleanField(default=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    # def __str__(self):
    #     return self.user1, self.user2
    #

class Message(models.Model):
    Room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    SenderIsCustomer =models.BooleanField(default=False)
    MessageText = models.CharField(max_length=10000)
    Seen = models.BooleanField(default=False)
    Deleted = models.BooleanField(default=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.Room



