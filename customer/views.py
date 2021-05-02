from django.shortcuts import render,redirect   # ek page se dusre pe bhejne k liye
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart   # it is used to make msg subparts like to from subject
from email.mime.text import MIMEText  # is used to add html content
import email.mime.application
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category,Products
from Manager.models import Series,Notifications,Order, Bill , Uploadedlist, Customer
import urllib.request
import re

sab=Products.objects.filter(Status__icontains="Available")

# ----------------------------------------for login--------------------------------------------------------- #
def handlelogin(request) :
    Blockbuster=Series.objects.filter(Type__icontains="Today's Blockbuster")
    latest=Series.objects.filter(Type__icontains="Latest TV Serials")
    cartoon=Series.objects.filter(Type__icontains="Best Cartoon forever")
    sports=Series.objects.filter(Type__icontains="Live Sports")
    allcat=Category.objects.all()
    if request.method=="POST" :
        username=request.POST.get("name","")
        password=request.POST.get("password","")
        user=authenticate(username=username,password=password) # it will check
        discount(request)
        if user is not None :
               login(request,user)
               Customer(Name=username).save()
               n=len(Notifications.objects.all())-Customer.objects.filter(Name=request.user)[0].notification_no
               messages.success(request,f"Welcome {request.user} ! You have {n} new notifications...")
               return render(request,"home/home.html",{"param":link(),"allcat":allcat,"Blockbuster":Blockbuster,"latest":latest,"cartoon":cartoon,"sports":sports,"us":request.user, "sab":sab,"total":notif(request),"no_order":no_order(request.user)})
        else :
            messages.error(request,"invalid user ")
            return redirect("/")
    elif request.user.is_authenticated  :  # it checks it is authenticated or not
         discount(request)
         return render(request,"home/home.html",{"param":link(),"allcat":allcat,"Blockbuster":Blockbuster,"latest":latest,"cartoon":cartoon,"sports":sports,"sab":sab,"us":str(request.user),"total":notif(request),"no_order":no_order(request.user)})
    else :
        messages.warning(request,"You are not logged-in to our website, please login first..")
        return redirect("/")



# ----------------------------------for catogry wise products display-------------------------------------------- #

def category(request,slug) :    # jo category di h usse related product dega
    discount(request)
    allp=Products.objects.filter(Othername__icontains=slug).filter(Status="Available").order_by("Price")
    # print(allp.objects.filter(Status="Available"))
    return render(request,"home/category.html",{"no_order":no_order(request.user),"total":notif(request),"allp":allp,"slug":slug,"param":link(),"sab":sab,"us":request.user})


#--------------------------------for a singal product.----------------------------------------------------------------------

# jaise hi innnercat m aya to kabhi request.user ka order ek bhi nahi exist h to ek dict creat
# karo then us dictionary ko content m dal do ab jo bhi product lega usse content m update karo
def innercat(request,slug2) :
    discount(request)
    p=Products.objects.filter(Othername__icontains=slug2)[0] #if slug2=chanadal then gives <QuerySet[<Products: Chana Dal>]>
    if not Order.objects.filter(Name=request.user).exists() :  # taking only chana data by <QuerySet [<Products: Chana Dal>]>[0]
        ord=Order(Name=request.user)
        ord.save()
    ordpro=Order.objects.filter(Name=request.user)[0]
    content=ordpro.order
    if request.method=="POST" :
        try :
           one=request.POST.get("one",0)
           num=request.POST.get("num",0)
           price=p.Dprice if p.Discount > 0 else p.Price
           li=[int(one),int(num),float(price)*(int(num)+int(one))]
           # if num =1 and price = 20 then li=[0,1,price*(1+0)] = li=[0,1,20]
           for i in content :    # jo bhi product h wo kabhi already content m h to use delete kr or fir se update kr
               if i == slug2 :
                   del content[i]
                   break
           print("list",li)
           content.update({p.Name:li})
           print("content",content)
           ordpro.order=content
           ordpro.save()
           return render(request,"home/innercat.html",{"total":notif(request),"p":p,"name":slug2,"param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})
        except Exception as e :
            messages.warning(request,"You entered incorrect data !")
            return redirect(f"/login/product/subcatagory/{slug2}")
    else :
       return render(request,"home/innercat.html",{"no_order":no_order(request.user),"total":notif(request),"p":p,"name":slug2,"param":link(),"sab":sab,"us":request.user})



#------------------------------------About us -----------------------------------------------------------#
def about(request) :
    allcat=Category.objects.all()
    return render(request,"home/about.html",{"param":link(),"allcat":allcat,"us":request.user, "sab":sab,"total":notif(request),"no_order":no_order(request.user)})


#----------------------------------------------Log out--------------------------------------------------------#

def handlelogout(request) :
    logout(request)
    messages.success(request,"Succesfully logged out ")
    return redirect("/")


#------------------------------------profile changing--------------------------------------------------------#

def profile(request) :
    discount(request)
    USER=User.objects.filter(username=request.user)[0]
    if request.method=="POST" :
        username=request.POST.get("username",USER.username)
        email=request.POST.get("email",USER.email)
        firstname=request.POST.get("firstname",USER.first_name)
        lastname=request.POST.get("username",USER.last_name)
        password=request.POST.get("password"," ")
        USER.username=username
        USER.email=email
        USER.first_name=firstname
        USER.last_name=lastname
        if password != " " and len(password) > 7 :
            USER.set_password(password)
            USER.save()
            messages.success(request,"succesfully Updated the Account .. ")
            return redirect("/login/profile")
        else :
            messages.error(request,"password must be more then 7 characters")
            return redirect("/login/profile")
    else :
        return render(request,"home/profile.html",{"sab":sab,"no_order":no_order(request.user),"userrr":USER,"total":notif(request),"param":link(),"us":request.user})


#------------------------------------kabhi koi si discount ka notification h ya nahi -----------------------------#

def notify(request) :
    discount(request)
    allnot=Notifications.objects.order_by('-DT')
    cust=Customer.objects.filter(Name=request.user)[0]
    notfic_no=cust.notification_no
    leng=len(allnot)-notfic_no
    cust.notification_no=len(allnot)
    cust.save()
    return render(request,"home/notify.html",{"no_order":no_order(request.user),"allnot":allnot,"total":0,"len":leng, "us":request.user,"sab":sab,"param":link()})


#-------------------------------------delete the product from bucket---------------------------------------------#

def delete(request,slug3) :
    ord=Order.objects.filter(Name=request.user)[0]
    a=Products.objects.filter(Othername__icontains=slug3)[0]
    for i in ord.order :
        if i== a.Name :
            del ord.order[i]
            if a.Name in ord.Free :
              del ord.Free[a.Name]
            ord.save()
            break
    return redirect("/login/bucket/")

#----------------------------------------------bucket items---------------------------------------------------#

def bucket(request) :      # ye jo bhi item bucket m h use dekhne k liye
    discount(request)
    if no_order(request.user) != 0:
       allorder=Order.objects.filter(Name=request.user)[0]
       return render(request,"home/bucket.html",{"total":notif(request),"allorder":allorder.order, "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})
    else :
        messages.warning(request,"Your Bucket Does not Contain anything yet, Please Search and Add some product to your shopping bucket !")
        return render(request,"home/bucket.html",{"total":notif(request), "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})


# -------------------------------------------- bill banaya hua page ---------------------------------------------#

def bill(request) :
    discount(request)
    noti=Notifications.objects.filter(Type="Price Discount on Total").order_by("-Limit")
    notip=Notifications.objects.filter(Type="Discount on Buying a Product")
    b=Bill.objects.filter(Name__icontains="RPM")[0]
    if request.method=="POST" :
        order=Order.objects.filter(Name=request.user)[0]
        order.Customer=request.POST.get("name",order.Customer)
        order.Email=request.POST.get("email",order.Email)
        order.Phone=request.POST.get("contact",order.Phone)
        order.Address=request.POST.get("address",order.Address)
        order.Pin=request.POST.get("pin",order.Pin)
        order.State=request.POST.get("state",order.State)
        order.City=request.POST.get("city",order.City)
        order.Date=datetime.datetime.now().date()
        if len(order.Phone)==10 and len(order.Pin)==6 and "@gmail.com" in order.Email :
            order.save()
            summ=gt=dis=0
            for i in order.order.values() :    # order object k order[1,1,100] m 3th means price ka sum krke gt m dal diya
                summ=summ+i[2]
                gt=summ
            for i in noti :
                if summ > i.Limit :
                    gt=float(float(summ)-(float(summ)*int(i.Discount)/100))
                    dis=i.Discount
                    break
            for i in notip :
                if i.Item in order.order :
                    content=order.Free
                    s=sum(order.order[i.Item][0:4])
                    if s >= i.How :
                        content.update({i.Free:[f"Get Free {i.Freenum} unit '{i.Free}' on buying of {i.How} unit '{i.Item}'"]})
                        order.Free=content
                        order.save()
            messages.success(request,"Data have been succesfully saved !")
            return render(request,"home/bill.html",{"sum":float(summ),"grand":gt,"dis":dis,"total":notif(request),"b_n":b.bill_no+1,"Customer":order,"allorder":order.order, "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})
        else :
            messages.error(request,"Incorrect details! please make sure you have enterd correct phone number or email or pin")
            allorder=Order.objects.filter(Name=request.user)[0]
            return render(request,"home/bucket.html",{"total":notif(request),"allorder":allorder.order, "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})


#---------------------------------------bucket khali karne k liye---------------------------------------------------#
def done(request) :
    b=Bill.objects.filter(Name__icontains="RPM")[0]
    b_n=b.bill_no+1
    b.bill_no=b_n
    b.save()
    a=Order.objects.filter(Name=request.user)[0]
    total=0
    for i in a.order.values() :
            total=total+i[2]
    from prettytable import PrettyTable
    tabular_fields = ["Prdouct Name", "No. of kg","No. of pcs","Price"]
    tabular_table = PrettyTable()
    tabular_table.field_names = tabular_fields
    for k,v in a.order.items() :
        tabular_table.add_row([k,v[0],v[1],v[2]])  # making table rows
    item=tabular_table.get_html_string()
    try :
                  lower=a.City.lower()
                  if lower in ["maheshwar","maheshwer","maheswar","maheswer"] :
                      sorry=""
                      receivers_mail = [a.Email, "govindamahajangkrpm@gmail.com"]
                  else :
                      sorry="Note: Sorry for inconvenience. But currently Our delivery service is not available everywhere, It is only available within the Maheshwar region"
                      receivers_mail = [a.Email]
                  sender_mail = 'mahajankiranamhs@gmail.com'
                   # Html document of bill for sending to user and owner. isme hamne %% isliye lagaya kyoki jb hm %s karke %(item) likh raha tha tn "unsupported format character ';' (0x3b) at index 664 " to hamne sab jagah %% use kiya
                  html1 = """
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        <style>
             table{ width:100%%;}
            .row{ width: 100%%; margin-left: 1px;}
            .main{margin-left: 80px; width: 90%%;}
            .shri{font-size: 30px; text-align: center; text-decoration: underline; }
            .name{font-size: 50px; text-align: center; text-decoration: underline; font-family:Georgia, 'Times New Roman', Times, serif ;}
            .col-sm-6,.col-sm-7,.col-sm-5,.col-lg-3{font-size: 20px; border-right: 1px solid black;border-bottom: 1px solid black; }
            .total{margin-left: 140px;}
            th{font-size:18px; width:25%%; }
            th,td{border:1px solid black;}
            td{font-size:18px;}
            tr{background-color:rgba(0, 0, 255, 0.123);}
            .total{font-size:18px}
            @media screen  and (max-width: 600px){
            table{  margin-left:0px;}
            .main{margin-left: 0px; width:100%% ;}
            .shri{font-size: 2.8vw; }
            .name{font-size: 2.8vw;}
            .col-sm-6,.col-sm-7,.col-sm-5,.col-lg-3{font-size:10px; }
            .total{font-size: 2vw;}
            th,td{border-bottom:1px solid black; font-size:2.4vw; border-left:1px solid black;}
             }
        </style>
    </head>

    <body>
        <div style="color: red; margin-top:3; margin-bottom : 4;" class="name">Your Bill Reciept</div>
        <div class="main" style="border: 1px solid black; background-color:rgba(0, 0, 255, 0.233);">
            <div class="shri" style="color: blue;">|| श्री गणेशाय नमः ||</div>
            <div class="name mb-3" style="color: blue;">MahajanKirana.Com Bill Reciept</div>
            <div class="row" style="border-top: 1px solid black;">
                <div class="col-sm-6 col-md-6 col-lg-6">Address : Ward no. 3, Bhagat Singh Marg, Maheshwar Dist-Khargone(M.P)</div>
                <div class="col-sm-6 col-md-6 col-lg-6">Send Mail :mahajankiranamhs@gmail.com or call Us : 9685607577 </div>
            </div>
            <div class="row" style="border-top: 1px solid black;">
                <div class="col-sm-3 col-md-3 col-lg-3 col-xs-6">Name : %s</div>
                <div class="col-sm-3 col-md-3 col-lg-3 col-xs-6">Date : %s</div>
                <div class="col-sm-3 col-md-3 col-lg-3 col-xs-6">Gstin : None</div>
                <div class="col-sm-3 col-md-3 col-lg-3 col-xs-6">Bill no: RPM-%s</div>
            </div>
            <div class="w3-responsive table mb-0 " >
                   %s
            </div>
            <div class="row w3-hover-gray" style="height: 30px; border-bottom: 1px solid black;">
                    <div class="col-sm-10 col-md-10 col-lg-10 total">Total : %d</div>
            </div>
            <div class="row" ">
                    <div class="col-sm-6 col-lg-6 col-md-6 ">Name  :  %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 ">Email  :  %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 col-xs-6">Address  :  %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 col-xs-6">City  :  %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 col-xs-6">State  :  %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 col-xs-6">Pin  :  %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 col-xs-6">Phone : %s</div>
                    <div class="col-sm-6 col-lg-6 col-md-6 col-xs-6">Date  :    %s </div>
            </div>
        </div>
        <div style="color: red; margin-top:3; margin-bottom : 4; text-align:left; font-size:2vw;" class="name">%s</div>
    </body>
</html>
"""%(a.Customer, str(a.Date), str(b.bill_no), item, total, a.Customer, a.Email, a.Address, a.City, a.State, str(a.Pin), str(a.Phone), str(a.Date), str(sorry) )
                  for i in receivers_mail :
                        msg = MIMEMultipart()
                        msg['From'] = "MahajanKirana.Com"
                        msg['To'] = i
                        msg['Subject'] = "Mahajan Kirana Bill reciept"
                        HTML_Contents = MIMEText(html1, 'html')
                        msg.attach(HTML_Contents)
                        obj = smtplib.SMTP('smtp.gmail.com',587)
                        obj.ehlo()
                        obj.starttls()
                        obj.login(sender_mail,"rpm*2001")
                        obj.sendmail(sender_mail,receivers_mail,msg.as_string())
                  obj.quit()
                  a.order={}
                  a.save()
                  messages.success(request,"Your Order will reach to your home within 1 day..")
                  return redirect("/login")
    except Exception as e :
             messages.error(request,"Can't send the bill ! please try again")
             return redirect("/login")

# ------------------------------------------Uploading the list -----------------------------------------#
def upload(request) :
    allcat=Category.objects.all()
    if request.method=="POST" :
        Name=request.POST.get("name"," ")
        Phone=request.POST.get("contact"," ")
        Address=request.POST.get("address"," ")
        Pin=request.POST.get("pin"," ")
        State=request.POST.get("state"," ")
        City=request.POST.get("city"," ")
        Date=datetime.datetime.now().date()
        img=request.FILES["imglist"]
        if len(Phone)==10 and len(Pin)==6 and str(img).split(".")[::-1][0]=="jpg" or str(img).split(".")[::-1][0]=="jpeg" or str(img).split(".")[::-1][0]=="png":
            Uploadedlist(Name=Name,Phone=Phone,Address=Address,Pin=Pin,State=State,City=City,ImageList=img).save()
            messages.success(request,"Your order will be delevered withing a day...")
            return redirect("/login")
        else :
            messages.warning(request,"Incorrect details, Please fill it again ... ")
            return redirect("/login/upload")
    else :
        return render(request,"home/upload.html",{"total":notif(request),"allcat":allcat, "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})

# -----------------------------------------------tv----------------------------------------------------#

def tv(request,video) :
        allcat=Category.objects.all()
        discount(request)
        if video=="0" :
            return render(request, "home/tv.html",{"leng":video, "video":video,"total":notif(request),"allcat":allcat, "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})
        if request.method=="POST" :
                video=request.POST.get("yousearch","comedy").replace(" ","")
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={video}")
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        messages.success(request,"please wait for a moment untill all youtube videos get loaded...")
        return render(request, "home/tv.html",{"video":video,"vid":video_ids,"leng":video_ids,"total":notif(request),"allcat":allcat, "param":link(),"sab":sab,"us":request.user,"no_order":no_order(request.user)})

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



# Category: बिस्कुट-Biscuits>, <Category: दाल - Dal>, <Category: चावल - Chawal>, <Category: नहाने का साबुन - Bathing Soap>, <C
# ategory: कपड़ेधोनेकासाबुन-WashingSoap>, <Category: दंतमंजन-ToothPaste>, <Category: मसाले-Spices>, <Category: चायपत्ती-Tea>,
#  <Category: केशतेल-Hairoil>, <Category: खानेकातेल-Edibleoil>, <Category: टूथब्रश-ToothBrush>, <Category: पूजा पाठ सामग्री>, <
# Category: चॉकलेट - chocolate>, <Category: कुरकुरे चिप्स - kurkure chips>, <Category: शैम्पू - Shampoo>, <Category: LEDlights>, <Category:
#  पापड़-Papad>, <Category: घी - Ghee>, <Category: मेहँदी-Mehandi>, <Category: नूडल्स - Noodles>, '...(remaining elements truncated)...'

# NAME =hindi - englih
# other = hindi-english categ ------------------------------------------------------------------



# def innercat(request,slug2) :
#     discount(request)
#     p=Products.objects.filter(Othername__icontains=slug2)[0] #if slug2=chanadal then gives <QuerySet[<Products: Chana Dal>]>
#     if not Order.objects.filter(Name=request.user).exists() :  # taking only chana data by <QuerySet [<Products: Chana Dal>]>[0]
#         ord=Order(Name=request.user)
#         ord.save()
#     ordpro=Order.objects.filter(Name=request.user)[0]
#     content=ordpro.order
#     if request.method=="POST" :
#         try :
#            one=request.POST.get("one",0)
#            two=request.POST.get("two",0)
#            three=request.POST.get("three",0)
#            num=request.POST.get("num",0)
#            price=p.Dprice if p.Discount > 0 else p.Price
#            li=[int(one),int(two),int(three),int(num),float(price)*(int(num)+int(one)*1+int(two)*5+int(three)*15)]
#            # if num =1 the li=[0,0,0,1,100]
#            for i in content :    # jo bhi product h wo kabhi already content m h to use delete kr or fir se update kr
#                if i == slug2 :
#                    del content[i]
#                    break

# def bill(request) :
#         if len(order.Phone)==10 and len(order.Pin)==6 and "@gmail.com" in order.Email :
#             order.save()
#             summ=gt=dis=0
#             for i in order.order.values() :    # order object k order[1,1,1,100] m 4th means price ka sum krke gt m dal diya
#                 summ=summ+i[4]
#                 gt=summ

# def done(requeset) :
#     b=Bill.objects.filter(Name__icontains="RPM")[0]
#     b_n=b.bill_no+1
#     b.bill_no=b_n
#     b.save()
#     a=Order.objects.filter(Name=requeset.user)[0]
#     total=0
#     for i in a.order.values() :
#             total=total+i[4]
#     from prettytable import PrettyTable
#     tabular_fields = ["Prdouct Name", "No. of 1kg pack", "No. of 5kg pack","No. of 15kg pack","No. of pcs","Price"]
#     tabular_table = PrettyTable()
#     tabular_table.field_names = tabular_fields
#     for k,v in a.order.items() :
#         tabular_table.add_row([k,v[0],v[1],v[2],v[3],v[4]])  # making table rows
#     item=tabular_table.get_html_string()

# नमस्ते महाजन किराना में आप सभी का स्वागत है| हमारी इस साइट पर कई प्रकार के सामान उपलब्ध  है जिसकी शुद्धता की 100% ग्यारंटी आपको मिलती है. इस साइट पर आप घर बैठे-बैठे आप अपना ऑर्डर दे सकते हैं और ऑर्डर देने के बाद Email पर जाकर अपना बिल देख सकते हैं. महाजन किराना पर आपको  कुछ ही समय में आपके ऑर्डर की फ्री  delivery की सुविधा उपलब्ध है
# यदि साइट पर कोई सा प्रोडक्ट उपलब्ध नहीं है तो आप उसकी एक अलग से लिस्ट बनाकर या चाहे तो सारे सामान की लिस्ट बनाकर " Upload List " पर अपनी लिस्ट आसानी से uplaod कर सकते हैं .
# किसी भी सामान की थोक की खरीदी पर delivery के समय बिल में विशेष छुट दी जाएगी |
