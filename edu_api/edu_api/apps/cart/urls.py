from django.urls import path

from cart import views

urlpatterns = [
    path("option/", views.CartView.as_view({'post': 'add_cart', "get": "list_cart",
                                            "patch": "updata_cart", "put": "put_cart"})),
    path("options/", views.CartView.as_view({"put": "put_expire", "get": "get_select_course", "post": "get_length"})),
]
