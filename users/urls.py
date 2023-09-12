# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('fb_example/', views.fb_example, name='fb_example'),
    path('register_email_or_phone/', views.register_email_or_phone, name='register_email_or_phone'),
    path('check_register_verification_code/',views.check_register_verification_code,name='check_register_verification_code'),
    path('register_user/',views.register_user,name='register_user'),
]