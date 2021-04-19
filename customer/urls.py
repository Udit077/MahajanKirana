from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.handlelogin,name="login"),
    path("product/<str:slug>",views.category,name="product"),            # product/dal
    path("product/subcatagory/<str:slug2>",views.innercat,name="inner"),  # product/dal/tuwar dal
    path("product/subcatagory/delete/<str:slug3>/",views.delete,name="inner"), #product/dal/delete/tuwar dal
    path("logout/",views.handlelogout,name="logout"),                     # logout the user
    path("profile/",views.profile,name="profile"),                        # for changing the profile
    path("notification/",views.notify,name="notify"),                     # discount notifications
    path("bucket/",views.bucket,name="bucket"),                           # items in bucket
    path("bill/",views.bill,name="bill"),                                 # bill of all the products
    path("done/",views.done,name="done"),
    path("tv/<str:video>",views.tv,name="tv"),                             # complete the bill or order
    path("about/",views.about,name="about"),
    path("upload/",views.upload,name="about")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)