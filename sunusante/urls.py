"""
URL configuration for sunusante project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rendezvous/', include('rendezvous.urls')),
    path('patients/', include('patients.urls')),
    path('personnel/', include('personnel.urls')),
]
