from django.contrib import admin
from django.urls import path, include
from .views import view_ats
 
urlpatterns = [
    path('', view_ats, name='ATS home'),
]