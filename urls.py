from django.contrib import admin
from django.urls import path , re_path
from django.conf.urls import include
from games import views

app_name="games"

urlpatterns = [
path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('ps_news/',views.ps_news,name='ps_news'),
    path('ps_trailers/',views.ps_trailers,name='ps_trailers'),
    path('ps/',views.ps,name='ps'),
    path('ps_recommend/',views.ps_recommend,name="ps_recommend"),
    path('xbox/',views.xbox,name='xbox'),
    path('xbox_news/',views.xbox_news,name='xbox_news'),
    path('xbox_trailers/',views.xbox_trailers,name='xbox_trailers'),
    path('xbox_recommend/',views.xbox_recommend,name='xbox_recommend'),
    path('xbox_suggestions/',views.xbox_suggestions,name='xbox_suggestions'),
    path('login/', views.loginPage, name='login'),
	path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
	path('user_index/',views.user_index , name='user_index'),
]
