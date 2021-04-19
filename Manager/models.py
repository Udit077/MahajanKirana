from django.db import models
from picklefield.fields import PickledObjectField

class Customer(models.Model) :
    Name=models.CharField(max_length=50,default="")
    notification_no=models.IntegerField(default=0)
    def __str__(self) :
        return self.Name

class Series(models.Model) :
    Type=models.CharField(max_length=20,default="")
    Name=models.CharField(max_length=50,default="")
    Image=models.ImageField(upload_to="blockbuster/",max_length=200)
    Search=models.CharField(max_length=200,default="")
    def __str__(self) :
        return self.Type

class Notifications(models.Model) :
      not_id = models.AutoField(primary_key=True,default=0)
      From = models.DateField(blank=True)
      To=models.DateField()
      DT=models.DateTimeField(blank=True)
      Content=models.TextField(max_length=1000,default="")
      Title=models.CharField(max_length=500,default="")
      Type=models.CharField(max_length=100,default="")
      Discount=models.IntegerField(default=0)
      Limit=models.IntegerField(default=0)
      Item=models.CharField(max_length=100,default=0)
      How=models.IntegerField(default=0)
      Free=models.CharField(max_length=100,default="")
      Freenum=models.IntegerField(default=0)
    #   Status=models.CharField(max_length=10,default="not_seen")
      def __str__(self) :
          return self.Title

class Order(models.Model) :
    bill_no = models.AutoField(primary_key=True)
    Name=models.CharField(max_length=40,default="")
    Customer=models.CharField(max_length=40,default="")
    Email=models.CharField(max_length=50,default="")
    Phone=models.IntegerField(default=0)
    Address=models.CharField(max_length=100,default="")
    Pin=models.IntegerField(default=0)
    State=models.CharField(max_length=40,default="")
    City=models.CharField(max_length=50,default="")
    order=PickledObjectField(default={})
    Date=models.DateField(auto_now_add=True,blank=True)
    Free=PickledObjectField(default={})
    def __str__(self) :
        return self.Name

class Bill(models.Model) :
    Name=models.CharField(max_length=3,default="RPM")
    bill_no=models.IntegerField(default=0)
    def __str__(self) :
        return str(self.bill_no)

class Uploadedlist(models.Model) :
    Name=models.CharField(max_length=40,default="")
    Phone=models.IntegerField(default=0)
    Address=models.CharField(max_length=100,default="")
    Pin=models.IntegerField(default=0)
    State=models.CharField(max_length=40,default="")
    City=models.CharField(max_length=50,default="")
    Date=models.DateField(auto_now_add=True,blank=True)
    ImageList=models.ImageField(upload_to="list/")
    def __str__(self) :
        return self.Name

# महाजन किराना में आप सभी का स्वागत है | हमारी इस साइट पर किराना सामान की विशाल श्रृंखला उपलब्ध है, जिसकी शुद्धता की 100% ग्यारंटी आपको यहाँ मिलती है | इस साइट पर घर बैठे-बैठे आप अपना ऑर्डर दे सकते हैं और ऑर्डर देने के बाद Email पर जाकर अपना बिल देख सकते हैं | महाजन किराना पर आपको कुछ ही समय में आपके ऑर्डर की फ्री home delivery की सुविधा उपलब्ध है | यदि साइट पर कोई सा प्रोडक्ट उपलब्ध नहीं है तो आप उसकी एक अलग से लिस्ट बनाकर या चाहे तो सारे सामान की लिस्ट बनाकर " Upload a List " पर अपनी लिस्ट की scanned copy आसानी से uplaod कर सकते हैं | किसी भी सामान की थोक की खरीदी पर delivery के समय बिल में विशेष छुट दी जाएगी | सधन्यवाद !! 🙏🏻 🙏🏻 🙏🏻 नमस्ते ! 🙏🏻