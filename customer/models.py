from django.db import models

# starting product modal here :
class Products(models.Model) :
    Id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=70,default="")
    Othername=models.TextField(max_length=200,default="")
    Photo=models.ImageField(upload_to="product/",max_length=200)
    Price=models.IntegerField(default="")
    Discount=models.IntegerField(default=0)
    Quantity=models.CharField(max_length=10,default="")
    Dprice=models.FloatField(default=0)
    Status=models.CharField(max_length=20,default="Available")
    def __str__(self) :
        return self.Name

class Category(models.Model) :
    Name=models.CharField(max_length=50,default="")
    Photo=models.ImageField(upload_to="category/",max_length=200)
    Other=models.TextField(max_length=200,default="")
    def __str__(self) :
        return self.Name
