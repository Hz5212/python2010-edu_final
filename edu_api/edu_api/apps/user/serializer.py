import re

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from user.models import UserInfo
from user.utils import get_user_by_account

from django_redis import get_redis_connection

class UserModelSerializer(ModelSerializer):
    sms_code = serializers.CharField(min_length=4, max_length=8, required=True, write_only=True)
    token = serializers.CharField(max_length=1024, read_only=True, help_text="返回前端的token")

    class Meta:
        model = UserInfo
        fields = ("phone", "password", "id", "username", "token", "sms_code")

        extra_kwargs = {
            "phone": {
                "write_only": True
            },
            "password": {
                "write_only": True
            },
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },

        }

    def validate(self, attrs):
        """验证用户提交的注册信息是否合法"""
        phone = attrs.get("phone")
        password = attrs.get("password")
        code = attrs.get("sms_code")
        print(code)

        # 验证手机号的格式
        if not re.match(r'^1[356789]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式有误")

        # 验证手机号是否被注册了
        try:
            user = get_user_by_account(account=phone)
        except:
            user = None

        if user:
            raise serializers.ValidationError("当前手机号已经被注册")

        # 验证密码格式
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{6,16}$', password):
            raise serializers.ValidationError("密码格式有误")

        # 验证用户提交的验证码是否正确
        connection = get_redis_connection("sms_code")
        redis_code = connection.get("mobile_%s" % phone)
        print(redis_code)

        if redis_code.decode() != code:
            # 为了防止破解  同一个验证码可以只允许验证5次
            redis_count = connection.get("count_%s" % phone)
            # 验证码使用次数+1
            if redis_count:
                connection.set("count%s" % phone, int(redis_count.decode()) + 1)
            else:
                connection.set("count%s" % phone, 1)
            if int(connection.get("count%s" % phone).decode()) > 5:
                connection.flushdb()
                raise serializers.ValidationError("同一验证码只允许验证5次")
                # return Response({'message': "检测输入验证码多次不正确，请重新获取！"}, status=http_status.HTTP_400_BAD_REQUEST)
            raise serializers.ValidationError("验证码不正确")

        #  注册成功后将验证码从redis中删除
        if redis_code.decode() == code:
            # 清除当前数据库里面所有的key
            connection.flushdb()

        return attrs

    def create(self, validated_data):
        """
        重写create方法，完成对象的保存  token的生成
        :param validated_data:
        :return: username id  token
        """
        phone = validated_data.get("phone")
        password = validated_data.get("password")

        # 设置默认用户名 密码加密
        username = phone
        hash_pwd = make_password(password)
        # 保存对象
        user = UserInfo.objects.create(phone=phone, username=username, password=hash_pwd)

        # 用户创建后为该用户生成token
        if user:
            from rest_framework_jwt.settings import api_settings
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            user.token = jwt_encode_handler(payload)

        return user
    
    
# 忘记密码
class ForgetPasswordSerializers(ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ["phone", "password"]

    def validate(self, attrs):
        """验证用户提交的注册信息是否合法"""
        phone = attrs.get("phone")
        password = attrs.get("password")
        code = attrs.get("sms_code")

        # 验证手机号的格式
        if not re.match(r'^1[356789]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式有误")

        # 验证手机号是否被注册了
        try:
            user = get_user_by_account(account=phone)
        except:
            user = None

        if not user:
            raise serializers.ValidationError("当前手机号不存在")

        # 验证密码格式
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{6,16}$', password):
            raise serializers.ValidationError("密码格式有误")

        # 验证用户提交的验证码是否正确
        connection = get_redis_connection("sms_code")
        redis_code = connection.get("mobile_%s" % phone)
        print(redis_code)

        if redis_code.decode() != code:
            # 为了防止破解  同一个验证码可以只允许验证5次
            redis_count = connection.get("count_%s" % phone)
            # 验证码使用次数+1
            if redis_count:
                connection.set("count%s" % phone, int(redis_count.decode()) + 1)
            else:
                connection.set("count%s" % phone, 1)
            if int(connection.get("count%s" % phone).decode()) > 5:
                connection.flushdb()
                raise serializers.ValidationError("同一验证码只允许验证5次")
                # return Response({'message': "检测输入验证码多次不正确，请重新获取！"}, status=http_status.HTTP_400_BAD_REQUEST)
            raise serializers.ValidationError("验证码不正确")

        #  验证成功后将验证码从redis中删除
        if redis_code.decode() == code:
            # 清除当前数据库里面所有的key
            connection.flushdb()
            attrs['password'] = make_password(password)
        return attrs


