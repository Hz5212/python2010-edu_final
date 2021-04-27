from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

from edu_api.settings import constants
from home.models import Banner, Nav
from home.serializers import BannerModelSerializer, NavModelSerializer


class BannerListView(ListAPIView):
    """轮播图信息"""
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("orders")[:constants.BANNER_NUM]
    serializer_class = BannerModelSerializer


class NavHeadListView(ListAPIView):
    """顶部导航栏信息信息"""
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=1).order_by("orders")
    serializer_class = NavModelSerializer


class NavFootListView(ListAPIView):
    """尾部导航栏信息信息"""
    queryset = Nav.objects.filter(is_show=True, is_delete=False, position=2).order_by("orders")
    serializer_class = NavModelSerializer