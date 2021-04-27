from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status

from edu_api.libs.geetest import GeetestLib
from user.utils import get_user_by_account

from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from django_redis import get_redis_connection
from edu_api.settings import constants
from edu_api.utils.message import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer, ForgetPasswordSerializers

import random


pc_geetest_id = "eceb3f15b58977f4ccbf2680069aa19d"
pc_geetest_key = "2193c33833d27bf218e80d400618f525"

"""极验验证码视图类"""
class CaptchaAPIView(APIView):

    user_id = 0
    status = False

    def get(self, request):
        """获取验证码方法"""

        account = request.query_params.get('account')
        # 根据前端输入的账号来获取对应的用户
        user = get_user_by_account(account)

        if user is None:
            return Response({"msg": "用户不存在"}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        # 构建一个验证码对象
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # 响应获取的数据
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        """比对验证码的方法"""
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        account = request.data.get("account")
        user = get_user_by_account(account)

        if user:
            result = gt.success_validate(challenge, validate, seccode, user.id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


"""用户视图类 """
class UserAPIView(CreateAPIView, UpdateAPIView):

    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


"""前端验证手机号 - 注册"""
class UserCheckAPIView(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.GET.get("phone")

        user = get_user_by_account(account=phone)
        if user:
            return Response({"message": "手机号已存在"}, status=http_status.HTTP_400_BAD_REQUEST)
        return Response({"message": "手机号未注册"}, status=http_status.HTTP_200_OK)


"""前端验证手机号 - 忘记密码"""
class UserUpAPIView(APIView):

    def get(self, request, *args, **kwargs):
        phone = request.GET.get("phone")

        user = get_user_by_account(account=phone)
        if not user:
            return Response({"message": "手机号未注册"}, status=http_status.HTTP_400_BAD_REQUEST)
        return Response({"message": "手机号正确"}, status=http_status.HTTP_200_OK)


"""短信验证码"""
class SendMessageAPIView(APIView):

    def get(self, request):
        """
        根据提供的手机号来发送验证码
        :param request:
        """

        # 获取redis链接
        redis_connection = get_redis_connection("sms_code")
        phone = request.query_params.get("phone")
        print(phone)
        # 1. 判断该手机号格式以及是否在60s内发送过验证码
        phone_code = redis_connection.get("sms_%s" % phone)

        # 2. 生成随机验证码
        if phone_code:
            return Response({"message": "您已经在60s内发送过验证码了~"}, status=http_status.HTTP_400_BAD_REQUEST)
        code = "%06d" % random.randint(0, 999999)

        # 3. 将验证码保存redis中
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex("mobile_%s" % phone, constants.MOBILE_EXPIRE_TIME, code)
        # 验证码次数限制
        # redis_connection.set("count_%s" % phone, constants.CODE_COUNT)
        redis_connection.setex("count_%s" % phone, constants.MOBILE_EXPIRE_TIME, constants.CODE_COUNT)

        # 4. 调用发送短信方法，完成发送
        message = Message(constants.API_KEY)
        status = message.send_message(phone, code)
        if status:
            # 5. 响应发送的结果
            return Response({"message": "发送短信成功"})
        return Response({"message": "发送短信失败"})


class PhoneLoginAPIView(APIView):
    def post(self,request):
        phone = request.data.get("username")
        code = request.data.get("code")
        print(phone)
        from django_redis import get_redis_connection
        connection = get_redis_connection("sms_code")
        redis_code = connection.get(f"mobile_{phone}")
        if not redis_code:
            return Response({"msg":"验证码已过期或不存在"}, status=http_status.HTTP_400_BAD_REQUEST)
        redis_code = redis_code.decode()
        redis_count = connection.get(f"count_{phone}")
        print(redis_count.decode())
        print(redis_code)
        if redis_code != code:
            redis_count = int(redis_count.decode())
            connection.setex(f"count_{phone}", 600, redis_count-1)
            if redis_count == 1:
                connection.delete(f"mobile_{phone}")
                connection.delete(f"mobile_{redis_code}")
                connection.delete(f"count_{phone}")
                return Response({"msg": "验证码错误次数过多，请重新发送"}, status=http_status.HTTP_400_BAD_REQUEST)
            return Response({"msg": f"验证码不正确请重新输入，剩余{redis_count-1}次机会"}, status=http_status.HTTP_400_BAD_REQUEST)
        user = UserInfo.objects.get(phone=phone)
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({"username": user.username, "token": token})