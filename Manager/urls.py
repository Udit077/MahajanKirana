from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.admin,name="admin"),
    path("latest/",views.latest,name="latest"),
    path("customer/",views.customer,name="customer"),
    path("addp/",views.product,name="customer"),
    path("addc/",views.catagory,name="customer"),
    path("Delete/",views.delet,name="delete"),
    path("notify/",views.notify,name="noti"),
    path("alter/",views.alter,name="alter"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)