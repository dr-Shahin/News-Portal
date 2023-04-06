from django.urls import path

from main import views

from django.conf import settings
from django.conf.urls.static import static


from django.conf.urls import handler404
from django.views import defaults
from .views import handler404
defaults.page_not_found = handler404
handler404 = views.handler404



urlpatterns = [
    #path("", views.post_list, name="post_list"),

    path("register/", views.register, name="register"),
    path("login_user/", views.login_user, name="login_user"),
    path("logout_user/", views.logout_user, name="logout_user"),

    
    # path('load',views.load_more, name="load"),
    path('',views.index, name="index"),
    path("xeberlenti/",views.xeberlenti, name="xeberlenti"),
    path("haqqimizda/",views.haqqimizda, name="haqqimizda"), 
    
    
    
    path("elaqe/",views.elaqe, name="elaqe"),
    path("reklam/",views.reklam, name="reklam"),

    path("elaqe/addrey",views.addrey, name="addrey"),
    path("elaqe/deleterey/<int:id>",views.deleterey, name="deleterey"),



    path("page/<int:id>",views.page, name="page"),
    path("deletepage/<int:id>",views.deletepage, name="deletepage"),


    path("kateqoriya/<int:id>/",views.kateqoriya, name="kateqoriya"),
    
   
    path("xeber/", views.xeber, name="xeber"),
    path("xeberadmin/", views.xeberadmin, name="xeberadmin"),

    path("addnews/", views.addnews, name="addnews"),
    path("delete/<int:id>",views.delete, name="delete"),
    path("delete1/",views.delete1, name="delete1")
]
