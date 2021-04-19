from django.contrib import admin
from .models import Series,Bill,Notifications,Order, Uploadedlist, Customer
# Register your models here.
admin.site.register(Series)
admin.site.register(Notifications)
admin.site.register(Order)
admin.site.register(Bill)
admin.site.register(Uploadedlist)
admin.site.register(Customer)