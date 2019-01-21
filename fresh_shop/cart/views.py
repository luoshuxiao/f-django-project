from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods


def add_cart(request):
    if request.method == 'POST':
        #  接受商品id值和商品数量
        #  组装存储一个商品格式 ： [ goods_id,num,is_select]
        goods_id = int(request.POST.get('goods_id'))
        goods_num = int(request.POST.get('goods_num'))
        goods_list = [goods_id, goods_num, 1]
        session_goods = request.session.get('goods')
        #  判断session中有无该商品
        if session_goods:
            #  2. 添加重复的商品则修改
            flag = True
            for se_goods in session_goods:
                if se_goods[0] == goods_id:
                    se_goods[1] += goods_num
                    flag = False
            if flag:
                #  1. 添加的商品不存在与购物车中，则新增
                session_goods.append(goods_list)
            request.session['goods'] = session_goods
            count = len(session_goods)
        else:
            # 第一次添加购物车，组装商品存储格式[[],[]]
            request.session['goods'] = [goods_list]
            count = 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


# 刷新购物车的数量
def cart_num(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        count =len(session_goods) if session_goods else 0
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def cart(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        #  设计我的购物车页面数据返回格式：[对象1，对象2，...]
        #   商品对象 -- >  [ 商品对象1，is_select,num, total_price]
        result = []
        if session_goods:
            for se_goods in session_goods:
                # se_goods为[goods_id, num, is_select]
                goods = Goods.objects.filter(pk=se_goods[0])[0]
                total_price = goods.shop_price * se_goods[1]
                data = [goods, se_goods[1], se_goods[2], total_price]
                result.append(data)
        return render(request, 'cart.html', {'result': result})

#  我的购物车商品复选框的选择总数，价格总和
def cart_price(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        #  商品件数
        all_total =len(session_goods) if session_goods else 0
        all_price = 0
        is_select_num = 0
        for se_goods in session_goods:
            #  se_goods为[ goods_id,num,is_select]
            if se_goods[2]:
                goods = Goods.objects.filter(pk=se_goods[0])[0]
                all_price += goods.shop_price * se_goods[1]
                is_select_num += 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'all_total': all_total,
                             'all_price': all_price, 'is_select_num': is_select_num})


# def change_cart(request):
#     if request.method == 'POST':
#         #  修改商品的数量和选择状态
#         #  修改session中商品信息，结构为：[ goods_id,num,is_select]
#
#         #  获取商品id 和 数量或者状态
#         goods_id = request.POST.get('goods_id')
#         goods_num = request.POST.get('goods_num')
#         goods_select = request.POST.get('goods_select')
#         #   修改 session值
#         session_goods = request.session.get('goods')
#         for se_goods in session_goods:
#             if se_goods[0] == goods_id:
#                 se_goods[1] = int(goods_num) if goods_num else se_goods[1]
#                 se_goods[2] = int(goods_select) if goods_select else se_goods[2]
#         request.session['goods'] = session_goods
#         return JsonResponse({'code': 200, 'msg': '请求成功'})
def change_cart(request):
    if request.method == 'POST':
        # 修改商品的数量和选择状态
        # 其实就是修改session中商品信息，结构为[goods_id, num, is_select]

        # 1. 获取商品id值和（数量或选择状态）
        goods_id = int(request.POST.get('goods_id'))
        goods_num = request.POST.get('goods_num')
        goods_select = request.POST.get('goods_select')
        # 2. 修改
        session_goods = request.session.get('goods')
        for se_goods in session_goods:
            if se_goods[0] == goods_id:
                se_goods[1] = int(goods_num) if goods_num else se_goods[1]
                se_goods[2] = int(goods_select) if goods_select else se_goods[2]
                total = Goods.objects.filter(id=goods_id)[0].shop_price * se_goods[1]
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功', 'total': round(total, 2)})


def del_goods(request):
    if request.method == 'POST':
        goods_id = int(request.POST.get('goods_id'))
        session_goods = request.session.get('goods')
        for se_goods in session_goods:
            if goods_id == se_goods[0]:
                session_goods.remove(se_goods)
                break
        request.session['goods'] = session_goods
        user_id = request.session.get('user_id')
        if user_id:
            ShoppingCart.objects.filter(goods_id=goods_id,user_id=user_id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def change_checkbox(request, id):
    """点击复选框修改数据库和session中对应商品的is_select"""
    if request.method == 'POST':
        session_goods = request.session.get('goods')
        user_id = request.session.get('user_id')
        db_table_goods = ShoppingCart.objects.filter(goods_id=id, user_id=user_id)
        for se_goods in session_goods:
            if se_goods[0] == id:
                se_goods[2] = 0 if se_goods[2] else 1
                break
        for db_goods in db_table_goods:
            if db_goods.goods_id == id:
                db_goods.is_select = 0 if db_goods.is_select else 1
                break
        return JsonResponse({'code': 200, 'msg': '请求成功'})
