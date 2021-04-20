from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib import messages
from email.mime.text import MIMEText  # is used to add html content
import smtplib
import random as rd
from django.contrib.auth import authenticate,login,logout
from email.mime.multipart import MIMEMultipart
from customer.models import Category,Products
from Manager.models import Series,Notifications,Order, Bill , Uploadedlist, Customer

sab=Products.objects.filter(Status="Available")
# -----------------------------------------for login page -------------------------------------------------------#
def first(request) :
    if request.user.is_authenticated :
        return redirect("login/")
    return render(request,"first.html")

# ---------------------------------------- handling signup ------------------------------------------------------#
def handlesignup(request) :
    if request.method=="POST" :
        username=request.POST.get("name","")
        password=request.POST.get("password","")
        email=request.POST.get("email","")
        if len(password) > 7 and "@gmail.com" in email :
           if User.objects.filter(username=username).exists():
               messages.warning(request,f"{username} already exits ! Please enter unique Username")
           else :
             myuser=User.objects.create_user(username,email=email ,password=password)
             myuser.first_name=username
             myuser.last_name=username
             myuser.save()
            #  ----------------------------------------------
             Blockbuster=Series.objects.filter(Type__icontains="Today's Blockbuster")
             latest=Series.objects.filter(Type__icontains="Latest TV Serials")
             cartoon=Series.objects.filter(Type__icontains="Best Cartoon forever")
             sports=Series.objects.filter(Type__icontains="Live Sports")
             allcat=Category.objects.all()
             user=authenticate(username=username,password=password) # it will check
             discount(request)
             if user is not None :
                    login(request,user)
                    Customer(Name=username).save()
                    n=len(Notifications.objects.all())-Customer.objects.filter(Name=request.user)[0].notification_no
                    messages.success(request,f"Welcome {request.user} ! You have {n} new notifications...")
                    return render(request,"home/home.html",{"param":link(),"allcat":allcat,"Blockbuster":Blockbuster,"latest":latest,"cartoon":cartoon,"sports":sports,"us":request.user, "sab":sab,"total":notif(request),"no_order":no_order(request.user)})
            #  ----------------------------------------------
        else :
           messages.error(request,f"{username} your details are incorect , check your details and register again !")
    return redirect("/")

#----------------------------------------- handling forgot password ---------------------------------------------#
def forgot(request) :
    if request.method=="POST" :
        name=request.POST.get("name","")
        email=request.POST.get("email","")
        a,b,c,d,e,f,g,h=rd.choices(population = ["g","o","v","d","s","n","e","h","a","S","r","m","u","d","i","t","j","k","H","z","b","c"],k =8)
        if User.objects.filter(username=name).exists() :
          us=User.objects.filter(username=name)[0]
          pa=a+b+c+d+e+f+g+h
          us.set_password(pa)
          us.save()
          try :
                  sender_mail = 'mahajankiranamhs@gmail.com'
                  receivers_mail = email
                  html1 = """
                  Dear, %s .
                  <p> Your request for new password have been accepted .<br> Now your new password is  <strong>%s</strong> . <br>
                  You can change this password after going to <strong>MahajanKirana.com</strong> account setting </p>
                  <br>  Best Regards,
                    """%(name,pa)
                  msg = MIMEMultipart()
                  msg['From'] = "MahajanKirana.Com"
                  msg['To'] = receivers_mail
                  msg['Subject'] = "Regarding Forgot password"
                  HTML_Contents = MIMEText(html1, 'html')
                  msg.attach(HTML_Contents)
                  obj = smtplib.SMTP('smtp.gmail.com',587)
                  obj.ehlo()
                  obj.starttls()
                  obj.login(sender_mail,"rpm*2001")
                  obj.sendmail(sender_mail,receivers_mail,msg.as_string())
                  obj.quit()
                  messages.success(request,"password have been reset !")
          except Exception as a :
                messages.error(request,"can't send email.! An error occured while sending mail. Please try again later...")
        else :
            messages.warning(request,"You are not our user . Don't try to do that thing")
            return redirect("/")
    return redirect("/")

#--------------------------------------------product or category--------------------------------------------------#
def link():    # create a dict then sari category le raha h fir uss category se related product le k dict bana raha
    param={}   # h like {category:[product1,product2 ..]} or use return kr raha h
    li=[]
    allcat=Category.objects.all()
    for i in allcat :
        allp=Products.objects.filter(Othername__icontains=str(i).replace(" ",""))
        li=[j for j in allp]
        param.update({i:li})
        li=[]
    return param

def notif(request):
    cust=Customer.objects.filter(Name=request.user)[0]
    allnseen=len(Notifications.objects.all())-cust.notification_no
    return allnseen

#-----------------------------------------------order length -------------------------------------------------#
def no_order(name) :    # ye Order model m (name) se registerd jo bhi user h uska object- leng.order lenght dega
    try :
      leng=Order.objects.filter(Name=name)[0]
      return len(leng.order)
    except :
        return 0

def discount(requeset) :
    n=Notifications.objects.all()
    try :
     for i in n :
        if str(i.To) < str(datetime.datetime.now().date()) :
            if i.Type == "Price Discount on Product" :
               p=Products.objects.filter(Name=i.Item)[0]
               p.Discount=0
               p.save()
            elif i.Type == "Price Discount on Catagory" :
                c=Products.objects.filter(Othername__icontains=i.Item)
                for j in c :
                    j.Discount=0
                    j.save()
            elif i.Type == "Discount on Buying a Product" :
                order=Order.objects.filter(Name=requeset.user)[0]
                del order.Free[i.Free]
                order.save()
                print(order.Free)
            i.delete()
            messages.warning(requeset,f"OOPS ! {i.Title} offer have been closed")
    except :
          return redirect("/")