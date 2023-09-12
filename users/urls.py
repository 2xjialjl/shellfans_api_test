# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register_email_or_phone/', views.register_email_or_phone, name='register_email_or_phone'),
    path('fb_example/',views.fb_example,name='fb_example'),
    path('send_login_email/',views.send_login_email,name='send_login_email'),
    path('check_login_email/',views.check_login_email,name='check_login_email')
]