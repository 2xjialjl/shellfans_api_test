from rest_framework import serializers
from .models import User  # 导入 User 模型

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'