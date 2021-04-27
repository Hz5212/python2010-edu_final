from django.urls import path
from rest_framework_jwt import views

from user import views as user_views

urlpatterns = [
    path("login/", views.obtain_jwt_token),
    path("login2/", user_views.PhoneLoginAPIView.as_view()),
    path("captcha/", user_views.CaptchaAPIView.as_view()),
    path("register/", user_views.UserAPIView.as_view()),
    path("check_phone/", user_views.UserCheckAPIView.as_view()),
    path("check_phone_up/", user_views.UserUpAPIView.as_view()),
    path("message/", user_views.SendMessageAPIView.as_view()),
]