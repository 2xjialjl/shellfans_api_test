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

@api_view(['POST'])
def check_email(request):
    # 检查数据库中是否存在相同的邮箱
    email = request.data.get('email')
    if User.objects.filter(email=email).exists():
        return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Email is available'})

@api_view(['POST'])
def check_phone(request):
    phone_number = request.data.get('phone_number')

    # 检查数据库中是否存在相同的手机号码
    if User.objects.filter(phone_number=phone_number).exists():
        return Response({'message': 'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # 生成随机的6位数字验证码
    verification_code = str(random.randint(100000, 999999))

    # 发送短信验证码
    sms_host = "api.e8d.tw"
    send_sms_url = f"https://{sms_host}/API21/HTTP/sendSMS.ashx"
    user_id = "sfrd"
    password = "K4NM_UypMIP2"
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
        # 设置验证码的有效期为 10 分钟
        expiration_time = datetime.now() + timedelta(minutes=10)
        # 将验证码和有效期存储到缓存中
        cache.set(phone_number, {'code': verification_code, 'expiration': expiration_time}, 600)
        # 寄送驗證碼
        response = requests.post(send_sms_url, data=post_data)
        # 寄送簡訊的狀態
        response.raise_for_status()
        # 返回响应，指示验证码已发送
        return Response({'message': 'Verification code sent'})
    except Exception as e:
        # 处理发送短信失败的情况
        return Response({'message': f'SMS sending failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def verify_and_register_user(request):
    # 获取post回来的数据
    data = request.data

    # 检查email与手机号码是否重复
    phone_number = data.get('phone_number')
    user = User.objects.filter(Q(email=data.get('email')) | Q(phone_number=phone_number)).first()

    if user:
        # 如果用户已存在，返回错误消息
        return Response({'error': 'User with this email or phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

    # 获取验证码
    cached_data = cache.get(phone_number)
    if cached_data is None:
        return Response({'error': 'Verification code not found or has expired'}, status=status.HTTP_400_BAD_REQUEST)

    cached_verification_code = cached_data.get('code')
    verification_code = data.get('verification_code')
    cached_expiration = timezone.make_aware(cached_data.get('expiration'))

    # 检查验证码是否匹配
    if verification_code != cached_verification_code:
        return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

    # 检查验证码是否过期
    if cached_expiration < timezone.now():
        return Response({'error': 'Verification code has expired'}, status=status.HTTP_400_BAD_REQUEST)

    # 创建新用户并保存数据
    new_user = User(
        email=data.get('email'),
        name=data.get('name'),
        gender=data.get('gender'),
        birthday=data.get('birthday'),
        phone_number=phone_number,
        profile_picture=data.get('profile_picture'),
        level=data.get('level'),
        is_email_verified=True,
        is_phone_verified=True,
    )
    new_user.save()

    # 注册成功后，从缓存中删除验证码
    cache.delete(phone_number)

    return Response({'message': 'Successfully registered'}, status=status.HTTP_201_CREATED)
@api_view(['POST'])
def fb_example(request):
    return Response({"algorithm": "HMAC-SHA256","expires": 1291840400,"issued_at": 1291836800,"user_id": "218471"}, status=status.HTTP_200_OK)