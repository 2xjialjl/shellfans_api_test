# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check_email/', views.check_email, name='check_email'),
    path('check_phone/', views.check_phone, name='check_phone'),
    path('verify_register_user/', views.verify_and_register_user, name='verify_and_register_user'),
    path('fb_example/',views.fb_example,name='fb_example'),
    path('test_email/',views.test_email,name='test_email')
]