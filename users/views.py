# users/views.py
import random
import requests
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import User, VerificationCode
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
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
        if not phone_number:
            response_data = {
                'result': False,
                'message': 'Email and phone are both empty',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
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
# 檢查驗證碼
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
                is_email_verified=False,
                is_phone_verified=True,
                privacy_agreement=True,
                terms_agreement=True,
                phone_region=data.get('country_code'),
            )
            new_user.save()
            # 刪除VerificationCode的資料
            VerificationCode.objects.filter(user_code=phone_number).delete()
            response_data = {
                'result': True,
                'message': 'User registration successful',
                'data': {
                    'code': status.HTTP_200_OK,
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except:
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
            # 創建用戶
            new_user = User(
                email=email,
                name=data.get('name'),
                gender=data.get('gender'),
                birthday=data.get('birthday'),
                phone_number=None,
                profile_picture='',
                level=0,
                is_email_verified=True,
                is_phone_verified=False,
                privacy_agreement=True,
                terms_agreement=True,
            )
            new_user.save()
            now = timezone.now()
            response_data = {
                'result': True,
                'message': 'User registration successful',
                'data': {
                    'code': status.HTTP_200_OK,
                    'time': now
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
    email = request.data.get('email')
    country_code = request.data.get('country_code')
    phone_number = request.data.get('phone_number')
    if not email:
        sent_phone_number = convert_country_code(phone_number, country_code)
        # 檢查有無手機號碼
        if User.objects.filter(phone_number=phone_number).exists():
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
        if User.objects.filter(email=email).exists():
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
                'message': 'Email is empty',
                'data': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'error': User.objects.filter(email=email).exists()
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# 檢查驗證碼
@api_view(['POST'])
def check_login_verification_code(request):
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