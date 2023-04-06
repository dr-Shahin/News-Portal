from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from .models import Newsdata, Mesaj, Koment
from django.contrib.auth.models import User, auth
from bs4 import BeautifulSoup
import requests
import json
import datetime as dt

from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactForm

from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import NewsdataSerializers


# class NewsdataViews(APIView):
#     def get(self, request, *args, **kwargs):


 




def post_list(request):
    numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'main/posts.html', {'numbers': numbers})




def handler404(request, exception):
    data = loader.render_to_string('main/404.html', {}, exception)
    return render(None, '404.html',data)
 

def haqqimizda(request):
    nsay =  Newsdata.objects.values_list("basliq").count()

    return render(request, 'main/haqqimizda.html',{"nsay":nsay})

def elaqe(request):
    form = ContactForm()
    blok1 = Newsdata.objects.all().order_by('-id')[0:3]

    reyler=Mesaj.objects.all().order_by('id')
    return render(request, 'main/elaqe.html',{'reyler':reyler, 'blok1':blok1, 'form':form})



def reklam(request):
    form = ContactForm()
    blok1 = Newsdata.objects.all().order_by('-id')[0:3]

    reyler=Mesaj.objects.all().order_by('id')
    return render(request, 'main/reklam.html',{'reyler':reyler, 'blok1':blok1, 'form':form})




def addrey(request):
    ad=request.POST['ad']
    email=request.POST['email']
    movzu=request.POST['movzu']
    mesaj=request.POST['mesaj']

    subject= [request.POST['ad'], request.POST['movzu'], request.POST['email']  ]
    mesage = "Hörmetli, "+ ad.upper() + " göndərdiyiniz "+ movzu.upper() + " -email müraciətə baxilacaq. Tezlikle sizə geri dönüş ediləcək. Köməyə ehtiyacınız varsa, lütfən, marketinq sualları üçün [e-poçt və telefon nömrəsi] ilə və ya mühasibat sualları üçün [e-poçt və telefon nömrəsi] ilə əlaqə saxlayın."
    
    email_from = settings.EMAIL_HOST_USER
    qebul_eden = [email,]
    qebul = ["sh96agayev@gmail.com",]
    send_mail(movzu,mesage,email_from,qebul_eden)

    add = Mesaj(ad=ad, email=email, movzu=movzu, mesaj=mesaj)
    add.save()
    send_mail(subject, mesaj, email_from, qebul)

    messages.success(request, 'Reyiniz uğurla əlavə edildi')
    return HttpResponseRedirect(reverse('elaqe'))



def deleterey(request,id):
    reyler=Mesaj.objects.get(id=id)
    reyler.delete()
    return HttpResponseRedirect(reverse('elaqe'))




def page(request, id):
    if request.method=="POST":
        ad=request.POST['name']
        email=request.POST['email']
        mesaj=request.POST['mesaj'] 
        movzu=request.POST['cari_rey']
        cari_id=request.POST['cari_id']

        add = Koment(ad=ad, email=email, movzu=movzu, mesaj=mesaj, cari_id=cari_id)
        add.save()

    blok01 = Newsdata.objects.raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')[0:7]
    blok02 = Newsdata.objects.raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id DESC ')

    blok = Newsdata.objects.all().order_by('-id')[0:1]
    blok1 = Newsdata.objects.all().order_by('-id')[0:4]
    blok2 = Newsdata.objects.all().order_by('id')[3:6]
    blok3 = Newsdata.objects.all().order_by('-id')[6:11]
    blok4 = Newsdata.objects.all().order_by('-id')[0:8]
    blok5 = Newsdata.objects.all().order_by('-id')[10:12]
    blok6 = Newsdata.objects.all().order_by('-id')[12:14]
    blok7 = Newsdata.objects.all().order_by('-id')[14:16]
    blok8 = Newsdata.objects.all().order_by('-id')[0:8]
    blok9 = Newsdata.objects.all().order_by('-id')[0:25]

    news = Newsdata.objects.filter(id=id)
    xeber = Newsdata.objects.get(id=id)
    koment = Koment.objects.filter(cari_id=id)
    
    title = xeber.basliq
    keys = title.split()
    
    acar = ''
    i = 0
    for n in keys:
        i+=1
        if i==1:
            acar = n
        else:
            acar = acar+', '+n
        
    
    return render(request,('main/page.html'),{"news":news, 'koment':koment, 'id':id, 'blok':blok, "blok1":blok1, 
    "blok2":blok2, "blok3":blok3, "blok4":blok4, "blok5":blok5, 'blok6':blok6, 
    'blok7':blok7,'blok8':blok8,'blok9':blok9, 'blok01':blok01, 'blok02':blok02,'acar':acar })



def deletepage(request,id):
    reyler=Koment.objects.get(id=id)
    reyler.delete()
    return HttpResponseRedirect(reverse('elaqe'))



def kateqoriya(request, id):
    blok01 = Newsdata.objects.raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')[0:7]
    r = Newsdata.objects.get(id=id)
    kat =r.kateqoriya

    news = Newsdata.objects.filter(kateqoriya=kat).distinct()

    news01 = Newsdata.objects.filter(kateqoriya=kat).distinct()[0:1]
    news02 = Newsdata.objects.filter(kateqoriya=kat).distinct()[1:5]
    news03 = Newsdata.objects.filter(kateqoriya=kat).distinct()[0:12]
    news04 = Newsdata.objects.filter(kateqoriya=kat).distinct()[12:24]

    son_xeber = Newsdata.objects.all().order_by('-id')[0:10]
    news_id = Newsdata.objects.filter(id=id)

    blok2 = Newsdata.objects.all().order_by('id')[3:6]

    return render(request,('main/kateqoriya.html'),
    {'news_id':news_id, 'son_xeber':son_xeber, 'news':news, 'news01':news01, 'news02':news02, 
    'news03':news03, 'news04':news04, 'blok01':blok01, "blok2":blok2 })


def xeberlenti(request):
    
    blok01 = Newsdata.objects.all().raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')[0:7]
    blok = Newsdata.objects.all().order_by('-id')[0:1]
    sondeq3 = Newsdata.objects.all().order_by('-id')[0:3]
    blok1 = Newsdata.objects.all().order_by('-id')[0:4]
    blok2 = Newsdata.objects.all().order_by('id')[3:6]
    blok3 = Newsdata.objects.all().order_by('-id')[1:2]
    blok4 = Newsdata.objects.all().order_by('-id')[2:4]
    blok5 = Newsdata.objects.all().order_by('-id')[2:4]
    blok6 = Newsdata.objects.all().order_by('-id')[6:9]
    blok7 = Newsdata.objects.all().order_by('-id')[9:12]

    nsay =  Newsdata.objects.values_list("basliq").count()
    blok8 = Newsdata.objects.all().order_by('-id')
    
    # Paginator in a view function to paginate a queryset
    page = request.GET.get('page', 1)
    paginator = Paginator(blok8, per_page=12)
    
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    blok9 = Newsdata.objects.all().order_by('-id')[0:4] 
    kat = Newsdata.objects.raw('SELECT * FROM main_newsdata WHERE kateqoriya ')
    news = Newsdata.objects.filter(kateqoriya=kat).distinct()
    news01 = Newsdata.objects.filter(kateqoriya=kat).distinct()[0:4]
    news02 = Newsdata.objects.filter(kateqoriya=kat).distinct()[1:5]
    news03 = Newsdata.objects.filter(kateqoriya=kat).distinct()[0:12]
    news04 = Newsdata.objects.filter(kateqoriya=kat).distinct()[12:24]
     
    context = {"sondeq3":sondeq3, "nsay":nsay, 'blok01':blok01, 'blok':blok, "blok1":blok1, "blok2":blok2, 
    "blok3":blok3, "blok4":blok4, "blok5":blok5, 'blok6':blok6, 'blok7':blok7,'blok8':blok8,
    'blok9':blok9, 'news':news, 'news01':news01, 'news02':news02, 'news03':news03, 'news04':news04,
    'numbers': numbers
     }  
    return render(request,('main/xeberlenti.html'),context)



def index(request):   
    blok01 = Newsdata.objects.all().raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')[0:7]
    blok02 = Newsdata.objects.all().raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')[7:12]
    blok03 = Newsdata.objects.all().raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')

    blok = Newsdata.objects.all().order_by('-id')[0:1]
    
    blok1 = Newsdata.objects.all().order_by('-id')[0:8]
    blok14 = Newsdata.objects.all().order_by('-id')[0:4]

    blok2 = Newsdata.objects.all().order_by('id')[3:6]
    blok3 = Newsdata.objects.all().order_by('-id')[1:2]
    blok4 = Newsdata.objects.all().order_by('-id')[2:4]
    blok5 = Newsdata.objects.all().order_by('-id')[2:4]
    blok6 = Newsdata.objects.all().order_by('-id')[6:9]
    blok7 = Newsdata.objects.all().order_by('-id')[9:12]

    blok8 = Newsdata.objects.all()

    obj_paginator = Paginator(blok8, 16)
    first_page = obj_paginator.page(1).object_list
    # range iterator of page numbers
    page_range = obj_paginator.page_range


    blok9 = Newsdata.objects.all().order_by('-id')[0:12]
    son8 = Newsdata.objects.all().order_by('-id')[4:12]
    
    kat = Newsdata.objects.raw('SELECT * FROM main_newsdata WHERE kateqoriya ')
    news = Newsdata.objects.filter(kateqoriya=kat).distinct()

    news01 = Newsdata.objects.filter(kateqoriya=kat).distinct()[0:4]
    news02 = Newsdata.objects.filter(kateqoriya=kat).distinct()[1:5]
    news03 = Newsdata.objects.filter(kateqoriya=kat).distinct()[0:12]
    news04 = Newsdata.objects.filter(kateqoriya=kat).distinct()[12:24]

    nsay = Newsdata.objects.values_list("basliq").count()
    

    #Hava proqnozu
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Baku,az&APPID=99714fa04d3d562ec0eb037231496d65")
    data = response.text  
    data  = json.loads(data)
    # print(data)
    temp = (data['main']['temp'] - 272.15 )
    temp = int(temp)
    city = data['name']  
    country= (data['sys']['country'])
    

    context = {'country':country, "city":city, "temp":temp, "son8":son8, "nsay":nsay, 'blok01':blok01,'blok02':blok02,'blok03':blok03, 
               'blok':blok, "blok1":blok1,"blok14":blok14, "blok2":blok2, "blok3":blok3, "blok4":blok4, "blok5":blok5, 'blok6':blok6, 
               'blok7':blok7,'blok8':blok8,'blok9':blok9, 'news':news, 'news01':news01, 'news02':news02, 'news03':news03, 'news04':news04,
               'obj_paginator':obj_paginator,
               'first_page':first_page,
               'page_range':page_range,
    # 'posts': post_obj, 
    # 'total_obj': total_obj 
    }

    if request.method == 'POST':
        #getting page number
        page_no = request.POST.get('page_no', None) 
        results = list(obj_paginator.page(page_no).object_list.values('id', 'link','basliq','foto', 'metn','kateqoriya', 'tarix'))
        return JsonResponse({"results":results})

    return render(request,('main/index.html'),context)



def xeber(request):
    my_news=Newsdata.objects.all().order_by('-id')[0:50]
    nsay = Newsdata.objects.values_list("basliq").count()
    template = loader.get_template("main/xeber.html")
    data = {"my_news": my_news, 'nsay':nsay}
    return HttpResponse(template.render(data,request))


def addnews(request):
    req = requests.get("https://metbuat.az/")
    soup = BeautifulSoup(req.text, 'html.parser')
    sayt= soup.find_all('a',attrs={"class":"news_box"})
    y=1
    for i in sayt:
        # qeyd
        w= i.find("h4",class_='news_box_ttl')
        # q= Newsdata.objects.filter("basliq")
        # if w!=q:
        link1= 'https://metbuat.az' + i["href"]
        data = requests.get(link1)
        soup = BeautifulSoup(data.content,'html.parser')

        w = soup.find('span',class_='news_in_catg')
        if w is not None:
            kat = w.text
        else:
            kat = None

        w = soup.find('article',class_='normal-text')
        if w is not None:
            metn = w.text
            metn= metn.replace("You must enable Javascript on your browser for the site to work optimally and display sections completely." ," ")
            
        else:
            metn = None
    
        image= i.find("img")
        image = 'https://metbuat.az/' + image["src"]
    
        w= i.find("h4",class_='news_box_ttl')
        if w is not None:
            title = w.text
        else:
            title = None
        
        x = dt.datetime.now()
        vaxt = (str(x.date()) + " " + x.strftime("%H") + ":" + x.strftime("%M"))
        # print(vaxt)

        add = Newsdata(link=link1, basliq=title, foto=image, metn=metn, tarix=vaxt, kateqoriya=kat)
        add.save()
        messages.success(request, 'Xeber uğurla əlavə edildi')
        if y==15:
            break
        else:
            y+=1
        # else:
        #     break       
    return HttpResponseRedirect(reverse('xeber'))




def delete(request, id):
    Newsdata.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('xeber'))



def delete1(self):
    Newsdata.objects.all().delete()
    return HttpResponseRedirect(reverse('xeber'))




def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Bu istifadeci artiq movcuddur')
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()    
                return redirect('login_user')
        else:
            messages.info(request, 'Parollar uygundur')
            return redirect("register")      
    else:
        return render(request, 'main/register.html')




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Login ve ya parol yanlishdir')
            return redirect('main/login_user')
    else:
        return render(request, 'main/login_user.html')


def logout_user(request):
    auth.logout(request)
    return redirect('index')



def axtar(request):
    if request.method == "POST":
        data1 = request.POST["sorgu"]
        my_xeber = Newsdata.objects.filter(Brand__contains=data1)
          
        template = loader.get_template("main/axtar.html")    
        data = {"my_xeber": my_xeber,  'data1':data1}
        return HttpResponse(template.render(data,request)) 
    else:
        return render(request, 'main/axtar.html',{})




def xeberadmin(request):
    my_xeber = Newsdata.objects.all().order_by('id')
    kat = Newsdata.objects.all().raw('SELECT * FROM main_newsdata GROUP BY kateqoriya ORDER BY id ASC ')
    reyler=Mesaj.objects.all().order_by('id')
    return render(request, 'main/xeberadmin.html',{'reyler':reyler, 'my_xeber':my_xeber,'kat':kat})