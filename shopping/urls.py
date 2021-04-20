from django.contrib import admin       # for django admin
from django.urls import path,include   # to include path of urls
from . import views                    # for views.py function
from django.conf import settings       # to use media files and static 
from django.conf.urls.static import static    


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.first,name="home"),
    path("signup/",views.handlesignup,name="sign"),
    path("login/",include("customer.urls")),
    path("Admin/",include("Manager.urls")),
    path("forgot/",views.forgot,name="forgot"),
 ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

