from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Message)
admin.site.register(Rooms)
admin.site.register(CustomerDetail)
admin.site.register(Dataforchat)

# class CustomerDetails(admin.ModelAdmin):
#     # readonly_fields = ('CreatedAt',)
#     list_display = ('customer_name', 'customer_phone', 'customer_email','Created')
#
#
# admin.site.register(ChatCustomerDetail,CustomerDetails)

# admin.site.register()


# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'display_genre')

# customer_name = models.CharField(max_length=50)
# customer_phone = models.CharField(max_length=50)
# customer_email = models.CharField(max_length=100)
# CreatedAt = models.DateTimeField(auto_now_add=True)