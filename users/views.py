# users/views.py
import random
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import User, VerificationCode
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
import jwt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken, Token
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import base64
import requests
import pymysql
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
@api_view(['GET'])
def fb_example(request):
    return Response({"algorithm": "HMAC-SHA256","expires": 1291840400,"issued_at": 1291836800,"user_id": "218471"}, status=status.HTTP_200_OK)

# 處理電話號碼
def convert_country_code(phone_number,country_code):
    # 定義一個dictory來處理轉換
    country_code_mapping = {
        'TW': '+886',# 將ZH轉換為+886
        'JP': '+81'
    }
    # 獲取轉換後的值，如果找不到則返回原始值
    converted_code = country_code_mapping.get(country_code, country_code)
    if converted_code.startswith('+886') and phone_number.startswith('0'):
        phone_number = converted_code + phone_number[1:]  # 去掉前面的 "0"

    return phone_number

# 註冊的寄發驗證信或簡訊
@api_view(['POST'])
def register_email_or_phone(request):
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')
    country_code = request.data.get('country_code')
    if not email:
        sent_phone_number = convert_country_code(phone_number, country_code)
        # 如果是手機號碼註冊,檢查手機號碼是否重複
        if not User.objects.filter(phone_number=phone_number).exists():
            # 生成隨機的6位數驗證碼
            verification_code = str(random.randint(100000, 999999))
            # 當前時間
            now = datetime.now()
            # 當前時間+10分鐘
            expiration_time = now + timedelta(minutes=10)
            # 發送簡訊驗證碼
            sms_host = "api.e8d.tw"
            send_sms_url = f"https://{sms_host}/API21/HTTP/sendSMS.ashx"
            user_id = "sfrd"
            password = "3nmWyb|iA5V2Ub"
            subject = "唄粉科技"
            content = f'你的簡訊驗證碼為: {verification_code}'
            mobile = sent_phone_number

            post_data = {
                "UID": user_id,
                "PWD": password,
                "SB": subject,
                "MSG": content,
                "DEST": mobile,
            }
            try:
                # 寄送驗證碼
                response = requests.post(send_sms_url, data=post_data)
                # 存到db
                verification_code_db = VerificationCode(user_code=phone_number, code=verification_code, expiration_time=expiration_time)
                verification_code_db.save()
                # 寄送簡訊的狀態
                response.raise_for_status()
                # 寄送簡訊成功
                response_correct_data = {
                    'result': True,
                    'message': 'Sending SMS successfully',
                    'data': {
                        'code': status.HTTP_200_OK,
                    }
                }
                return Response(response_correct_data, status=status.HTTP_200_OK)
            except Exception:
                # 寄送簡訊失敗
                response_error_data = {
                    'result': False,
                    'message': 'SMS server error',
                    'data': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }
                }
                return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # 檢查email是否重複
        if not User.objects.filter(email=email).exists():
            # 生成隨機的6位數驗證碼
            verification_code = str(random.randint(100000, 999999))
            # 當前時間
            now = datetime.now()
            # 當前時間+10分鐘
            expiration_time = now + timedelta(minutes=10)
            # 發送email
            html_message = render_to_string('email_register_template.html', {'verification_code': verification_code})
            subject = 'shellfans 註冊驗證信'
            from_email = 'hello@shell.fans'
            recipient_list = [email]
            try:
                send_mail(subject, html_message, from_email, recipient_list, fail_silently=False, html_message=html_message)
                # 存到db
                verification_code_db = VerificationCode(user_code=email, code=verification_code, expiration_time=expiration_time)
                verification_code_db.save()
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
                    'message': 'Email or Database server error',
                    'data': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                'result': False,
                'message': 'Email or phone has be registered',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# 註冊的檢查驗證碼
@api_view(['POST'])
def check_register_verification_code(request):
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')
    code = request.data.get('verification_code')
    if not email:
        verification_codes = VerificationCode.objects.filter(user_code=phone_number, code=code)
        if not verification_codes.exists():
            # 驗證碼不存在,驗證失敗
            response_data = {
                'result': False,
                'message': 'Invalid verification code',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # 驗證碼是否過期
        now = timezone.now()
        valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
        if not valid_verification_codes.exists():
            response_data = {
                'result': False,
                'message': 'Verification code has expired',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            'result': True,
            'message': 'Verification code is valid',
            'data': {
                'code': status.HTTP_200_OK,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        verification_codes = VerificationCode.objects.filter(user_code=email, code=code)
        if not verification_codes.exists():
            # 無email,驗證失敗
            response_data = {
                'result': False,
                'message': 'Invalid email verification code',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'verification_codes': verification_codes,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 驗證碼是否過期
        now = timezone.now()
        valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
        if not valid_verification_codes.exists():
            response_data = {
                'result': False,
                'message': 'Email verification code has expired',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            'result': True,
            'message': 'Verification code is valid',
            'data': {
                'code': status.HTTP_200_OK,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

# 註冊所有資料帶入資料庫
@api_view(['POST'])
def register_user(request):
    data = request.data
    email = data.get('email')
    phone_number = data.get('phone_number')
    now = datetime.now()
    if not email:
        try:
            # 創建用戶
            new_user = User(
                email=None,
                name=data.get('name'),
                gender=data.get('gender'),
                birthday=data.get('birthday'),
                phone_number=data.get('phone_number'),
                profile_picture='',
                level=0,
                created_at=now,
                is_email_verified=False,
                is_phone_verified=True,
                privacy_agreement=True,
                terms_agreement=True,
                phone_region=data.get('country_code'),
                third_party_registration_source='0'
            )
            new_user.save()
            # 刪除VerificationCode的資料
            VerificationCode.objects.filter(user_code=phone_number).delete()
            user = get_object_or_404(User, phone_number=phone_number)
            user_id = user.user_id
            payload = {
                'id': user_id
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response_data = {
                'result': True,
                'message': 'User registration successful',
                'data': {
                    'code': status.HTTP_200_OK,
                    'token': token
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            # db server error
            response_error_data = {
                'result': False,
                'message': 'DB server error',
                'data': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            }
            return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        try:
            now = datetime.now()
            # 創建用戶
            new_user = User(
                email=email,
                name=data.get('name'),
                gender=data.get('gender'),
                birthday=data.get('birthday'),
                phone_number=None,
                profile_picture='',
                level=0,
                created_at=now,
                is_email_verified=True,
                is_phone_verified=False,
                privacy_agreement=True,
                terms_agreement=True,
                third_party_registration_source='0'
            )
            new_user.save()
            # 刪除VerificationCode的資料
            VerificationCode.objects.filter(user_code=email).delete()
            user = get_object_or_404(User, email=email)
            user_id = user.user_id
            payload = {
                'id': user_id
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response_data = {
                'result': True,
                'message': 'User registration successful',
                'data': {
                    'code': status.HTTP_200_OK,
                    'token':token
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            # db server error
            response_error_data = {
                'result': False,
                'message': 'DB server error',
                'data': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            }
            return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 登入的寄發驗證信或簡訊
@api_view(['POST'])
def login_email_or_phone(request):
    accout = request.data.get('account')
    if '@' not in accout:
        # 檢查有無手機號碼
        if User.objects.filter(phone_number=accout).exists():
            user = User.objects.get(phone_number=accout)
            phone_number = user.phone_number
            country_code = user.phone_region
            sent_phone_number = convert_country_code(phone_number, country_code)
            # 生成隨機的6位數驗證碼
            verification_code = str(random.randint(100000, 999999))
            # 當前時間
            now = datetime.now()
            # 當前時間+10分鐘
            expiration_time = now + timedelta(minutes=10)
            # 發送簡訊驗證碼
            sms_host = "api.e8d.tw"
            send_sms_url = f"https://{sms_host}/API21/HTTP/sendSMS.ashx"
            user_id = "sfrd"
            password = "3nmWyb|iA5V2Ub"
            subject = "唄粉科技"
            content = f'你的簡訊驗證碼為: {verification_code}'
            mobile = sent_phone_number

            post_data = {
                "UID": user_id,
                "PWD": password,
                "SB": subject,
                "MSG": content,
                "DEST": mobile,
            }
            try:
                # 寄送驗證碼
                response = requests.post(send_sms_url, data=post_data)
                # 存到db
                verification_code_db = VerificationCode(user_code=phone_number, code=verification_code, expiration_time=expiration_time)
                verification_code_db.save()
                # 寄送簡訊的狀態
                response.raise_for_status()
                # 寄送簡訊成功
                response_correct_data = {
                    'result': True,
                    'message': 'Sending SMS successfully',
                    'data': {
                        'code': status.HTTP_200_OK,
                    }
                }
                return Response(response_correct_data, status=status.HTTP_200_OK)
            except Exception:
                # 寄送簡訊失敗
                response_error_data = {
                    'result': False,
                    'message': 'SMS server error',
                    'data': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }
                }
                return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                'result': False,
                'message': 'Phone is empty',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    else:
        # 檢查有無email
        if User.objects.filter(email=accout).exists():
            # 生成隨機的6位數驗證碼
            verification_code = str(random.randint(100000, 999999))
            # 當前時間
            now = datetime.now()
            # 當前時間+10分鐘
            expiration_time = now + timedelta(minutes=10)
            # 發送email
            html_message = render_to_string('email_login_template.html', {'verification_code': verification_code})
            subject = 'shellfans 登入驗證信'
            from_email = 'hello@shell.fans'
            recipient_list = [accout]
            try:
                send_mail(subject, html_message, from_email, recipient_list, fail_silently=False, html_message=html_message)
                # 存到db
                verification_code_db = VerificationCode(user_code=accout, code=verification_code, expiration_time=expiration_time)
                verification_code_db.save()
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
                    'message': 'Email or Database server error',
                    'data': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                'result': False,
                'message': 'Email is empty',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# 登入的檢查驗證碼
@api_view(['POST'])
def check_login_verification_code(request):
    accout = request.data.get('account')
    code = request.data.get('verification_code')
    if '@' not in accout:
        verification_codes = VerificationCode.objects.filter(user_code=accout, code=code)
        if not verification_codes.exists():
            # 驗證碼不存在,驗證失敗
            response_data = {
                'result': False,
                'message': 'Invalid verification code',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        # 驗證碼是否過期
        now = timezone.now()
        valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
        if not valid_verification_codes.exists():
            response_data = {
                'result': False,
                'message': 'Verification code has expired',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, phone_number=accout)
        user_id = user.user_id
        payload = {
            'user_id': user_id
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response_data = {
            'result': True,
            'message': 'Verification code is valid',
            'data': {
                'code': status.HTTP_200_OK,
                'token': token
            }
        }
        # 刪除VerificationCode的資料
        VerificationCode.objects.filter(user_code=accout).delete()
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        verification_codes = VerificationCode.objects.filter(user_code=accout, code=code)
        if not verification_codes.exists():
            # 無email,驗證失敗
            response_data = {
                'result': False,
                'message': 'Invalid email verification code',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'verification_codes': verification_codes,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 驗證碼是否過期
        now = timezone.now()
        valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
        if not valid_verification_codes.exists():
            response_data = {
                'result': False,
                'message': 'Email verification code has expired',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=accout)
        user_id = user.user_id
        payload = {
            'user_id': user_id
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response_data = {
            'result': True,
            'message': 'Verification code is valid',
            'data': {
                'code': status.HTTP_200_OK,
                'token': token
            }
        }
        # 刪除VerificationCode的資料
        VerificationCode.objects.filter(user_code=accout).delete()
        return Response(response_data, status=status.HTTP_200_OK)

# 快速註冊
@api_view(['POST'])
def quick_registration(request):
    data = request.data
    email = data.get('email')
    # 檢查email是否重複
    if not User.objects.filter(email=email).exists():
        try:
            new_user = User(
                email=email,
                name=data.get('name'),
                gender=None,
                birthday=None,
                phone_number=None,
                profile_picture='',
                level=0,
                is_email_verified=False,
                is_phone_verified=False,
                privacy_agreement=False,
                terms_agreement=False,
                phone_region='',
                third_party_registration_source=data.get('third_party_registration_source')
            )
            new_user.save()
            user_id = new_user.user_id
            payload = {
                'user_id': user_id
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            response_data = {
                'result': True,
                'message': 'User registration successful',
                'data': {
                    'code': status.HTTP_200_OK,
                    'token': token
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except:
            # db server error
            response_error_data = {
                'result': False,
                'message': 'DB server error',
                'data': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR
                }
            }
            return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        user = get_object_or_404(User, email=email)
        user_id = user.user_id
        payload = {
            'user_id': user_id
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response_data = {
            'result': True,
            'message': 'Verification code is valid',
            'data': {
                'code': status.HTTP_200_OK,
                'token': token
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

# 呼叫token
@api_view(['GET'])
def get_user_info(request):
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        response_data = {
            'result': False,
            'message': 'Token is missing in the headers',
            'data': {
                'code': status.HTTP_401_UNAUTHORIZED,
            }
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
    try:
        authorization_parts = authorization_header.split()
        if len(authorization_parts) != 2:
            response_data = {
                'result': False,
                'message': 'Invalid Authorization header format',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 獲取 Token
        _, token = authorization_parts
        token = str(token).replace("Bearer ", '')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        # Token過期
        response_data = {
            'result': False,
            'message': 'Token error',
            'data': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        # Token無效
        response_data = {
            'result': False,
            'message': 'Invalid token',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
                'token':token,
                'error':str(e)
            }
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(user_id=payload.get('user_id')).first()
    if not user:
        # 找不到user
        response_data = {
            'result': False,
            'message': 'User not found',
            'data': {
                'code': status.HTTP_404_NOT_FOUND,
            }
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    info = serializer.data
    name = info.get('name')
    email = info.get('email')
    gender = info.get('gender')
    birthday = info.get('birthday')
    phone_number = info.get('phone_number')
    profile_picture = info.get('profile_picture')
    level = info.get('level')
    is_email_verified = info.get('is_email_verified')
    is_phone_verified = info.get('is_phone_verified')
    third_party_registration_source = info.get('third_party_registration_source')
    backup_email = info.get('backup_email')
    is_backup_email_verified = info.get('is_backup_email_verified')
    security_code = info.get('security_code')
    response_data = {
        'result': True,
        'message': 'User information retrieved successfully',
        'data': {
            'name': name,
            'email': email,
            'gender': gender,
            'birthday': birthday,
            'phone_number': phone_number,
            'profile_picture': profile_picture,
            'level': level,
            'is_email_verified': is_email_verified,
            'is_phone_verified': is_phone_verified,
            'third_party_registration_source': third_party_registration_source,
            'backup_email': backup_email,
            'is_backup_email_verified': is_backup_email_verified,
            'security_code': security_code
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)

# 交換token
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def refresh_token(request):
    try:
        authorization_header = request.headers.get('Authorization')
        _, token = authorization_header.split()
        decoded_payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user_id = decoded_payload.get('user_id')
        user = User.objects.get(user_id=user_id)
        refresh_token = RefreshToken().for_user(user)
        refresh_token['user_id'] = user.user_id
        new_access_token = str(refresh_token.access_token)
        response_data = {
            'result': True,
            'message': 'Token refresh successful',
            'data': {
                'code': status.HTTP_200_OK,
                'token': new_access_token,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        response_data = {
            'result': False,
            'message': 'Token refresh failed',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
                'error': str(e),

            }
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# 編輯個人資料的寄發驗證信或簡訊
@api_view(['POST'])
def edit_profiles_sent_verification_code(request):
    accout = request.data.get('account')
    phone_region = request.data.get('country_code')
    if '@' not in accout:
        # 檢查有無手機號碼
        if not User.objects.filter(phone_number=accout).exists():
            sent_phone_number = convert_country_code(accout, phone_region)
            # 生成隨機的6位數驗證碼
            verification_code = str(random.randint(100000, 999999))
            # 當前時間
            now = datetime.now()
            # 當前時間+10分鐘
            expiration_time = now + timedelta(minutes=10)
            # 發送簡訊驗證碼
            sms_host = "api.e8d.tw"
            send_sms_url = f"https://{sms_host}/API21/HTTP/sendSMS.ashx"
            user_id = "sfrd"
            password = "3nmWyb|iA5V2Ub"
            subject = "唄粉科技"
            content = f'你的簡訊驗證碼為: {verification_code}'
            mobile = sent_phone_number
            post_data = {
                "UID": user_id,
                "PWD": password,
                "SB": subject,
                "MSG": content,
                "DEST": mobile,
            }
            try:
                # 寄送驗證碼
                response = requests.post(send_sms_url, data=post_data)
                # 存到db
                verification_code_db = VerificationCode(user_code=accout, code=verification_code, expiration_time=expiration_time)
                verification_code_db.save()
                # 寄送簡訊的狀態
                response.raise_for_status()
                # 寄送簡訊成功
                response_correct_data = {
                    'result': True,
                    'message': 'Sending SMS successfully',
                    'data': {
                        'code': status.HTTP_200_OK,
                    }
                }
                return Response(response_correct_data, status=status.HTTP_200_OK)
            except Exception:
                # 寄送簡訊失敗
                response_error_data = {
                    'result': False,
                    'message': 'SMS server error',
                    'data': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }
                }
                return Response(response_error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                'result': False,
                'message': 'Phone is empty',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    else:
        # 檢查有無email
        if not User.objects.filter(email=accout).exists():
            # 生成隨機的6位數驗證碼
            verification_code = str(random.randint(100000, 999999))
            # 當前時間
            now = datetime.now()
            # 當前時間+10分鐘
            expiration_time = now + timedelta(minutes=10)
            # 發送email
            html_message = render_to_string('email_login_template.html', {'verification_code': verification_code})
            subject = 'shellfans 登入驗證信'
            from_email = 'hello@shell.fans'
            recipient_list = [accout]
            try:
                send_mail(subject, html_message, from_email, recipient_list, fail_silently=False, html_message=html_message)
                # 存到db
                verification_code_db = VerificationCode(user_code=accout, code=verification_code, expiration_time=expiration_time)
                verification_code_db.save()
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
                    'message': 'Email or Database server error',
                    'data': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    }
                }
                return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response_data = {
                'result': False,
                'message': 'Email is empty',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# 編輯個人資料
@api_view(['PUT'])
def edit_profiles(request):
    authorization_header = request.headers.get('Authorization')
    if not authorization_header:
        response_data = {
            'result': False,
            'message': 'Token is missing in the headers',
            'data': {
                'code': status.HTTP_401_UNAUTHORIZED,
            }
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
    try:
        authorization_parts = authorization_header.split()
        if len(authorization_parts) != 2:
            response_data = {
                'result': False,
                'message': 'Invalid Authorization header format',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        # 獲取 Token
        _, token = authorization_parts
        token = str(token).replace("Bearer ", '')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        # Token過期
        response_data = {
            'result': False,
            'message': 'Token error',
            'data': {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except jwt.DecodeError:
        # Token無效
        response_data = {
            'result': False,
            'message': 'Invalid token',
            'data': {
                'code': status.HTTP_400_BAD_REQUEST,
            }
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    user_id = payload.get('id')
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        if 'name' in request.data:
            name = request.data.get('name')
            user.name = name
        if 'gender' in request.data:
            gender = request.data.get('gender')
            user.gender = gender
        if 'email' in request.data:
            email = request.data.get('email')
            code = request.data.get('verification_code')
            verification_codes = VerificationCode.objects.filter(user_code=email, code=code)
            if not verification_codes.exists():
                # 驗證碼不存在,驗證失敗
                response_data = {
                    'result': False,
                    'message': 'Invalid verification code',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # 驗證碼是否過期
            now = timezone.now()
            valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
            if not valid_verification_codes.exists():
                response_data = {
                    'result': False,
                    'message': 'Verification code has expired',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                response_data = {
                    'result': False,
                    'message': 'Email is empty',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            user.email = email
        if 'backup_email' in request.data:
            backup_email = request.data.get('backup_email')
            code = request.data.get('verification_code')
            verification_codes = VerificationCode.objects.filter(user_code=backup_email, code=code)
            if not verification_codes.exists():
                # 驗證碼不存在,驗證失敗
                response_data = {
                    'result': False,
                    'message': 'Invalid verification code',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # 驗證碼是否過期
            now = timezone.now()
            valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
            if not valid_verification_codes.exists():
                response_data = {
                    'result': False,
                    'message': 'Verification code has expired',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            user.backup_email = backup_email
        if 'phone_number' in request.data:
            phone_number = request.data.get('phone_number')
            code = request.data.get('verification_code')
            country_code = request.data.get('country_code')
            verification_codes = VerificationCode.objects.filter(user_code=phone_number, code=code)
            if not verification_codes.exists():
                # 驗證碼不存在,驗證失敗
                response_data = {
                    'result': False,
                    'message': 'Invalid verification code',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            # 驗證碼是否過期
            now = timezone.now()
            valid_verification_codes = verification_codes.filter(expiration_time__gte=now)
            if not valid_verification_codes.exists():
                response_data = {
                    'result': False,
                    'message': 'Verification code has expired',
                    'data': {
                        'code': status.HTTP_400_BAD_REQUEST,
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            user.phone_number = phone_number
            user.country_code = country_code
        security_code = request.data.get('security_code')
        user.security_code = security_code
        if 'profile_picture'in request.data:
            profile_picture = request.data.get('profile_picture')
            user.profile_picture = profile_picture
        user.save()
        response_data = {
            'result': True,
            'message': 'edit_profiles is successfully',
            'data': {
                'code': status.HTTP_200_OK,
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

# 爬蟲寄出錯誤信件
def send_email(subject, body, to_email):
    outlook_user = 'jason.huang@shell.fans'
    outlook_password = '2Xjialjl@'
    msg = MIMEMultipart()
    msg['From'] = outlook_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(outlook_user, outlook_password)

    server.sendmail(outlook_user, to_email, msg.as_string())
    server.quit()

# fb爬蟲
@api_view(['POST'])
def fb_crawler(request):
    options = Options()
    # 關閉瀏覽器跳出訊息
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    # options.add_argument("--headless")  # 不開啟實體瀏覽器背景執行
    options.add_argument("--incognito")  # 開啟無痕模式
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    # 設定要開啟的網頁
    driver.get("https://zh-tw.facebook.com/")
    # 等待時間
    time.sleep(1)
    # 填寫帳號密碼
    # 帳號
    driver.find_element(By.ID, "email").send_keys("rd@shell.fans")
    # 密碼
    driver.find_element(By.NAME, "pass").send_keys("Xzg7&OxwDmqj")
    # 點擊登入
    driver.find_element(By.NAME, "login").click()
    time.sleep(2)
    group_uid = '108718772321057'
    driver.get("https://www.facebook.com/profile.php?id=" + group_uid)
    time.sleep(2)
    driver.find_element(By.XPATH, "//*[text()='切換']").click()
    time.sleep(3)
    driver.find_element(By.XPATH, "//*[text()='Switch']").click()
    time.sleep(3)
    driver.get('https://www.facebook.com/profile.php?id=' + group_uid + '&sk=followers')
    # 等待時間
    time.sleep(3)

    # 初始化滾動次數和儲存資料的計數器
    scroll_count = 0
    max_scroll_count = 5  # 每滾動幾次存一次資料
    # 使用 JavaScript 執行滾動直到頁面底部
    last_height = driver.execute_script("return document.body.scrollHeight;")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # 等待頁面加載，可以根據需要調整等待時間
        new_height = driver.execute_script("return document.body.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height
        scroll_count += 1
        if scroll_count == max_scroll_count:
            # 讀取網頁內容
            soup = BeautifulSoup(driver.page_source)
            # 抓取粉絲專頁名稱
            group_name = soup.find('div', class_='x1e56ztr x1xmf6yo').text
            first_user_id = soup.find_all('div', class_="x1iyjqo2 x1pi30zi")
            # 抓取使粉絲姓名
            user_name_list = []
            for j in first_user_id:
                user_name_list.append(j.find('span',
                                             class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text)
            # 抓取使粉絲uid
            user_uid = []
            for i in first_user_id:
                user_uid.append(i.find('a')['href'].replace('https://www.facebook.com/profile.php?id=', ''))
            # 抓取使粉絲大頭照並轉換成base64
            user_image_list = []
            find_image = soup.find_all('img', class_='x1lq5wgf xgqcy7u x30kzoy x9jhf4c x9f619 xl1xv1r')
            if len(find_image) != 0:
                for index, image in enumerate(find_image):
                    img = requests.get(image["src"]).content
                    base64_encoded = base64.b64encode(img).decode('utf-8')
                    user_image_list.append(base64_encoded)
            data_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            scroll_count = 0  # 重設滾動次數
            # 儲存資料到資料庫
            try:
                conn = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='user',
                                       charset='utf8')
                cursor = conn.cursor()
                for uid, name, image_base64 in zip(user_uid, user_name_list, user_image_list):
                    insert_query = f"INSERT IGNORE fb_fan_uid (group_uid,group_name,uid, user_name, user_headshot,create_time) VALUES ('{group_uid}','{group_name}','{uid}', '{name}', '{image_base64}','{data_time}')"
                    cursor.execute(insert_query)
                    conn.commit()
            except Exception as e:
                subject_failure = "程式執行失敗通知"
                body_failure = f"程式執行時發生錯誤: {e}"
                to_email_failure = "jason.huang@shell.fans"
                send_email(subject_failure, body_failure, to_email_failure)
            finally:
                if conn:
                    conn.close()

    if driver:
        driver.close()
    subject_success = "程式正確執行通知"
    body_success = "您的程式已正確執行。"
    to_email_success = "jason.huang@shell.fans"
    send_email(subject_success, body_success, to_email_success)

