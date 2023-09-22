# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('fb_example/', views.fb_example, name='fb_example'),
    path('register_email_or_phone/', views.register_email_or_phone, name='register_email_or_phone'),
    path('check_register_verification_code/',views.check_register_verification_code,name='check_register_verification_code'),
    path('register_user/',views.register_user,name='register_user'),
    path('login_email_or_phone/',views.login_email_or_phone,name='login_email_or_phone'),
    path('check_login_verification_code/',views.check_login_verification_code,name='check_login_verification_code'),
    path('quick_registration/',views.quick_registration,name='quick_registration'),
    path('get_user_info/',views.get_user_info,name='get_user_info'),
    path('edit_profiles/',views.edit_profiles,name='edit_profiles'),
    path('edit_profiles_sent_verification_code/',views.edit_profiles_sent_verification_code,name='edit_profiles_sent_verification_code'),
    path('fb_crawler/',views.fb_crawler,name='fb_crawler'),
]