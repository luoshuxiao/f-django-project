from django.urls import path
from cart import views
urlpatterns = [
    #  添加购物车
    path('add_cart/', views.add_cart, name='add_cart'),
    #  购物车数量
    path('cart_num/', views.cart_num, name='cart_num'),
    #  购物车
    path('cart/', views.cart, name='cart'),
    #  购物车计算价格
    path('cart_price/', views.cart_price, name='cart_price'),
    #  修改购物车中的商品数量、选择状态
    path('change_cart/', views.change_cart, name='change_cart'),
    #  删除购物车商品
    path('del_goods/', views.del_goods, name='del_goods'),
    #  复选框更新状态（更新数据库和session）
    path('change_checkbox/<int:id>/', views.change_checkbox, name='change_checkbox'),
]