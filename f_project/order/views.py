# -*- coding: utf-8 -*-

"""与订单相关的视图函数"""

from django.urls import reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect


from user.models import UserAddress
from cart.models import ShoppingCart
from order.models import OrderInfo
from order.models import OrderGoods
from order.function import get_order_sn


def place_order(request):
    """订单金额、数量、总计"""
    if request.method == 'GET':
        # 获取当前登录用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True)
        total_price = 0
        num = 0
        user_address = user.useraddress_set.all()
        if carts.first():
            for cart in carts:
                #  小计金额
                price = cart.goods.shop_price * cart.nums
                cart.goods_price = price
                #  总金额
                num += 1
                total_price += price
            return render(request, 'place_order.html', {'carts': carts, 'total_price': total_price,
                                                        'num': num, 'user_address': user_address})
        else:
            return HttpResponseRedirect(reverse('cart:cart'))


def order(request):
    """创建订单（购物车提交成功后）"""
    if request.method == 'POST':
        #  获取收货地址id值
        #  创建订单
        #  创建订单详情
        ad_id = request.POST.get('ad_id')
        user_id = request.session.get('user_id')
        order_sn = get_order_sn()
        shop_cart = ShoppingCart.objects.filter(user_id=user_id,
                                                is_select=True)
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums
        user_address = UserAddress.objects.filter(pk=ad_id).first()
        order = OrderInfo.objects.create(user_id=user_id, order_sn=order_sn, order_mount=order_mount,
                                         address=user_address.address, signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        # 创建订单的详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 删除购物车和session中已经提交订单的商品
        shop_cart.delete()
        session_goods = request.session.get('goods')
        for se_goods in session_goods[:]:
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg':'请求成功'})