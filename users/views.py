# users/views.py
import random
import requests
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import User
from django.utils import timezone
from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import render_to_string
@api_view(['POST'])
def check_email(request):
    # 檢查email是否重複
    email = request.data.get('email')
    if User.objects.filter(email=email).exists():
        response_error_data = {
            'result': False,
            'message': 'Email already exists',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)
    response_correct_data = {
        'result': True,
        'message': 'Email does not exist',
        'data': {
            'code': status.HTTP_200_OK,
        }
    }
    return Response(response_correct_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def check_phone(request):
    phone_number = request.data.get('phone_number')
    # 檢查資料庫是否有相同資料
    if User.objects.filter(phone_number=phone_number).exists():
        response_error_data = {
            'result': False,
            'message': 'Phone Number already exists',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    # 生成隨機的6位數驗證碼
    verification_code = str(random.randint(100000, 999999))

    # 發送簡訊驗證碼
    sms_host = "api.e8d.tw"
    send_sms_url = f"https://{sms_host}/API21/HTTP/sendSMS.ashx"
    user_id = "sfrd"
    password = "3nmWyb|iA5V2Ub"
    subject = "唄粉科技"
    content = f'你的簡訊驗證碼為: {verification_code}'
    mobile = phone_number

    post_data = {
        "UID": user_id,
        "PWD": password,
        "SB": subject,
        "MSG": content,
        "DEST": mobile,
    }
    try:
        # 驗證碼的有效期 10 分鐘
        expiration_time = datetime.now() + timedelta(minutes=10)
        # 驗證碼存入cache中
        cache.set(phone_number, {'code': verification_code, 'expiration': expiration_time}, 600)
        # 寄送驗證碼
        response = requests.post(send_sms_url, data=post_data)
        # 寄送簡訊的狀態
        response.raise_for_status()
        cached_data = cache.get(phone_number)
        # 寄送簡訊成功
        response_correct_data = {
            'result': True,
            'message': 'Sending SMS successfully',
            'data': {
                'code': status.HTTP_200_OK,
            }
        }
        return Response(response_correct_data, status=status.HTTP_200_OK)
    except Exception as e:
        # 寄送簡訊失敗
        response_error_data = {
            'result': False,
            'message': 'Sending SMS error',
            'data': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        }
        return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def verify_and_register_user(request):
    # 取post回来的數據
    data = request.data
    # 檢查email與手機號碼是否重複
    phone_number = data.get('phone_number')
    user = User.objects.filter(Q(email=data.get('email')) | Q(phone_number=phone_number)).first()

    if user:
        # 如果用user存在，返回錯誤
        response_error_data = {
            'result': False,
            'message': 'Email or Phone Number already exists',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    # 從cach中拿取驗證碼
    cached_data = cache.get(phone_number)
    if cached_data is None:
        response_error_data = {
            'result': False,
            'message': 'Verification code not found or has expired',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    cached_verification_code = cached_data.get('code')
    verification_code = data.get('verification_code')
    cached_expiration = timezone.make_aware(cached_data.get('expiration'))

    # 檢查驗證碼是否正確
    if verification_code != cached_verification_code:
        response_error_data = {
            'result': False,
            'message': 'Invalid verification code',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    # 检查驗證碼是否過期
    if cached_expiration < timezone.now():
        response_error_data = {
            'result': False,
            'message': 'Verification code has expired',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    # 創建用戶
    new_user = User(
        email=data.get('email'),
        name=data.get('name'),
        gender=data.get('gender'),
        birthday=data.get('birthday'),
        phone_number=phone_number,
        profile_picture='',
        level=0,
        is_email_verified=False,
        is_phone_verified=True,
    )
    new_user.save()

    # 註冊成功後刪除cache
    cache.delete(phone_number)
    response_correct_data = {
        'result': True,
        'message': 'Successfully registered',
        'data': {
            'code': status.HTTP_200_OK,
        }
    }
    return Response(response_correct_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def fb_example(request):
    return Response({"algorithm": "HMAC-SHA256","expires": 1291840400,"issued_at": 1291836800,"user_id": "218471"}, status=status.HTTP_200_OK)
@api_view(['POST'])
def send_login_email(request):
    email = request.data.get('email')
    # 檢查email是否存在資料庫內
    if User.objects.filter(email=email).exists():
        # 生成隨機的6位數驗證碼
        login_verification_code = str(random.randint(100000, 999999))
        # 驗證碼的有效期 10 分鐘
        login_expiration_time = datetime.now() + timedelta(minutes=10)
        # 驗證碼存入cache中
        cache.set(email, {'code': login_verification_code, 'expiration': login_expiration_time}, 600)
        # 發送email
        email = request.data.get('email')
        verification_code = str(random.randint(100000, 999999))
        # 發送email
        html_message = render_to_string('email_template.html', {'verification_code': verification_code})
        subject = 'shellfans 登入驗證信'
        from_email = 'hello@shell.fans'
        recipient_list = [email]
        try:
            send_mail(subject, html_message, from_email, recipient_list, fail_silently=False, html_message=html_message)
            response_correct_data = {
                'result': True,
                'message': 'Sending email successfully',
                'data': {
                    'code': status.HTTP_200_OK,
                    'data':login_verification_code
                }
            }
            return Response(response_correct_data, status=status.HTTP_200_OK)
        except Exception:
            response_data = {
                'result': False,
                'message': 'Email server error',
                'data': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        response_error_data = {
            'result': False,
            'message': 'Email already exists',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def check_login_email(request):
    email = request.data.get('email')
    # 從cach中拿取驗證碼
    cached_data = cache.get(email)
    if cached_data is None:
        response_error_data = {
            'result': False,
            'message': 'Verification code not found or has expired',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    cached_verification_code = cached_data.get('code')
    #verification_code = data.get('verification_code')
    cached_expiration = timezone.make_aware(cached_data.get('expiration'))

    # 檢查驗證碼是否正確
    if email != cached_verification_code:
        response_error_data = {
            'result': False,
            'message': 'Invalid verification code',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    # 检查驗證碼是否過期
    if cached_expiration < timezone.now():
        response_error_data = {
            'result': False,
            'message': 'Verification code has expired',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_error_data, status=status.HTTP_400_BAD_REQUEST)

    # 註冊成功後刪除cache
    cache.delete(email)
    response_correct_data = {
        'result': True,
        'message': 'Successfully registered',
        'data': {
            'code': status.HTTP_200_OK,
        }
    }
    return Response(response_correct_data, status=status.HTTP_200_OK)
@api_view(['POST'])
def test_email(request):
    email = request.data.get('email')
    verification_code = str(random.randint(100000, 999999))
    # 發送email
    html_message = render_to_string('email_template.html', {'verification_code': verification_code})
    subject = 'shellfans 登入驗證信'
    from_email = 'hello@shell.fans'
    recipient_list = [email]
    try:
        send_mail(subject, html_message, from_email, recipient_list, fail_silently=False, html_message=html_message)
        response_correct_data = {
            'result': True,
            'message': 'Sending email successfully',
            'data': {
                'code': status.HTTP_200_OK,
            }
        }
        return Response(response_correct_data, status=status.HTTP_200_OK)
    except Exception:
        response_data = {
            'result': False,
            'message': 'Email server error',
            'data': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)