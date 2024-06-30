"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Landing, name='exercise_landingPage'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('user_input/', views.user_input, name='user_input'),
    path('bucket/', views.BucketPage, name='bucket'),
    # youtube
    path('index/', views.index, name='index'),
    path('favorite_videos/', views.favorite_videos, name='favorite_videos'),
    path('remove_favorite/', views.remove_favorite, name='remove_favorite'),
    path('add_to_favorites/<str:video_id>/',
         views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:video_id>/',
         views.remove_from_favorites, name='remove_from_favorites'),


]
