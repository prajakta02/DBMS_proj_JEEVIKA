"""jeevika URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from . import views

app_name='home'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('medicine/',views.medicine1,name='medicine'),
    path('blood/',views.blood1,name='blood'),
    path('four/',views.four,name='four'),
    path('request/',views.Request,name='request'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('update/',views.update,name='update'),
    path('delete/',views.delete,name='delete'),
    path('accept/',views.accept,name='accept'),
    path('accepted/',views.accepted,name='accepted')


]
