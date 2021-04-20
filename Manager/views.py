from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Series,Notifications
import os
import datetime
from customer.models import Category,Products
# ---------------------------------------------admin site pe jane k liuye-----------------------------------------#
def admin(request) :
    return render(request,"admin/home.html")

#----------------------------------movies, serial. cartoons k liye ------------------------------------------------#
def latest(request) :
    if request.method=="POST" :
        Type=request.POST.get("type","")
        alll=Series.objects.filter(Type=Type)
        location=f"C:/Users/admin//Desktop/coding/python+django+html+css/django/online/media"
        for i in alll :
            path = os.path.join(location,str(i.Image))  
            os.remove(path) 
            i.delete()
        ou=request.POST.get("1u","")
        oi=request.FILES['1i']
        tu=request.POST.get("2u","")
        ti=request.FILES['2i']
        thu=request.POST.get("3u","")
        thi=request.FILES['3i']
        fu=request.POST.get("4u","")
        fi=request.FILES['4i']
        fiu=request.POST.get("5u","")
        fii=request.FILES['5i']
        Series(Type=Type,Search=ou,Image=oi).save() 
        Series(Type=Type,Search=tu,Image=ti).save()
        Series(Type=Type,Search=thu,Image=thi).save()
        Series(Type=Type,Search=fu,Image=fi).save()
        Series(Type=Type,Search=fiu,Image=fii).save()
        messages.success(request,f"All {Type} are uploaded ")
        return redirect("/Admin")
    else :
        return render(request,"admin/latest.html")

#-------------------------------customer ko dekhne k liye -----------------------------------------------------------#
def customer(request) :
    allcust = User.objects.all()
    paginator = Paginator(allcust, 10) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/customer.html', {'page_obj': page_obj})

#-------------------------------------------product add karne k liye -----------------------------------------------#
def product(request) :
    if request.method=="POST" :
        cat=request.POST.get("cat","")
        name=request.POST.get("name","")
        oname=request.POST.get("oname","")
        price=request.POST.get("price","")
        image=request.FILES["image"]
        qua=request.POST.get("quantity","")
        cat=str(cat).replace(" ","")
        nname=str(name).replace(" ","")+" "+str(cat).replace(" ","")
        Products(Name=name,Othername=nname,Price=price,Quantity=qua,Photo=image).save()
        messages.success(request,"Product have been succefully added to our Database")
        return redirect("/Admin/addp")
    else :
        allcat=Category.objects.all()
        return render(request,"admin/product.html",{"allcat":allcat})

#--------------------------------------------category add karna------------------------------------------------------#
def catagory(request) :
    if request.method=="POST" :
        name=request.POST.get("name","")
        Photo=request.FILES["image"]
        Category(Name=name,Photo=Photo).save()
        messages.success(request,"Category have been succefully added to our Database")
        return redirect("/Admin")
    else :
        return render(request,"admin/category.html")

#-------------------------------------------notifications dalne -----------------------------------#
def notify(request) :
    allcat=Category.objects.all()
    allp=Products.objects.all()
    noti=Notifications()
    if request.method == "POST" :
        noti.Title=request.POST.get("title","")
        noti.Content=request.POST.get("content","")
        to=request.POST.get("to","")
        fromm=request.POST.get("fromm","")
        a1,b1,c1=to.split("-")
        noti.To=datetime.date(int(a1),int(b1),int(c1))
        a1,b1,c1=fromm.split("-")
        noti.From=datetime.date(int(a1),int(b1),int(c1))
        noti.Type=request.POST.get("type","")
        noti.Discount=request.POST.get("discount",0)
        noti.DT=datetime.datetime.now()
        if noti.Type == "Price Discount on Catagory"  : 
             noti.Item=request.POST.get("cat","")
             cat=request.POST.get("cat","")
             cust=Products.objects.filter(Othername__icontains=cat)
             for c in cust :
              c.Discount=noti.Discount
              c.Dprice=int(c.Price)-(int(noti.Discount)*int(c.Price))/100
              c.save()
        elif noti.Type == "Price Discount on Product" :
             noti.Item=request.POST.get("pro","")
             pro=request.POST.get("pro","")
             c=Products.objects.filter(Name=pro)[0]
             c.Discount=noti.Discount
             c.Dprice=int(c.Price)-(int(noti.Discount)*int(c.Price))/100
             print("kimat",c.Price,(int(noti.Discount)*int(c.Price))/100)
             c.save()
        elif noti.Type == "Price Discount on Total" :
             noti.Limit=request.POST.get("total",0)
        else :
             noti.Item=request.POST.get("buy","")
             noti.How=request.POST.get("how",0)
             noti.Free=request.POST.get("free","")
             noti.Freenum=request.POST.get("howfree",0)
        noti.save()
        messages.success(request,"successfully uploade discount")
        return render(request,"admin/notify.html",{"allcat":allcat,"allp":allp})
    else :
        return render(request,"admin/notify.html",{"allcat":allcat,"allp":allp})

#------------------------------------------delete the category-----------------------------------------------------#
def delet(request) :
    if request.method=="POST" :
        slug=request.POST.get("p","")
        delete=Products.objects.filter(Othername__icontains=slug)[0]
        file = str(delete.Photo)
        print(file)
        location = f"C:/Users/admin/Desktop/coding/python+django+html+css/django/online/media/"
        path = os.path.join(location, file)  
        os.remove(path) 
        delete.delete()
        messages.success(request,"Product have been succefully deleted")
        return redirect("/Admin")
    else :
        allp=Products.objects.all()
        return render(request,"admin/delet.html",{"sab":allp})
   
def alter(request) :
    if request.method=="POST" :
        name=request.POST.get("name","")
        # cname=request.POST.get("cname","n")
        # cother=request.POST.get("cother","n")
        status=request.POST.get("status","")
        price=request.POST.get("price")
        p=Products.objects.filter(Name=name)[0]
        # p.Name=cname
        # p.Othername=cother
        p.Status=status
        if int(price)!=0 :
            p.Price=int(price)
        p.save()
        return redirect("/Admin/alter")
    else :
        sab=Products.objects.filter(Status="Unavailable")
        return render(request,"admin/alter.html",{"sab":sab})

# advance sabhar  15g 10
# punjabi garam 100g 
# sambrani cup
# pitambari