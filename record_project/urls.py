"""
URL configuration for record_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls import handler404, handler500
from record_app import views
from record_app.hdss_backend import HdssStaffAuthenticationBackend
from record_app.views import register, facility_staff_login,dashboard_facility
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('register/', register, name='register'),
    path('/register/index.html', views.home, name='home_redirect'),
    path('/logout/register/', views.home, name='home_redirect2'),
    path('login/', views.facility_staff_login, name='facility_staff_login'),
    path('hdss/login/', views.hdss_staff_login, name='hdss_staff_login'),
    path('chat/', views.chat_view, name='chat_view'),
    path('hdss/', views.hdss_view, name='hdss_view'),
    path('dashboard_facility/', views.dashboard_facility, name='dashboard_facility'),
    path('logout/', views.logout, name='logout'),
    path('/logout/index.html', views.home, name='home_redirectt'),
    
]

# Serving static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)