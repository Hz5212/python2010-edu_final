from django.urls import path

from home import views

urlpatterns = [
    path("image/", views.BannerListView.as_view()),
    # 获取顶部导航栏信息信息
    path("hand/", views.NavHeadListView.as_view()),
    # 获取尾部导航栏信息信息
    path("foot/", views.NavFootListView.as_view()),
]