import re

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

from cart.models import ShoppingCart
from user.models import User


class StateMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id)[0]
            request.user = user
        # 2. 登录校验 ，需要区分那些地址需要登录校验，那些地址不需要做登录校验
        path = request.path
        #  用 in 逻辑运算符校验地址(不能用/user/.*/匹配，只能一一列出每个地址)
        # if path in ['/user/login/', '/user/register/', '/goods/index/', '/goods/detail/1/', '/cart/cart/']:
        #     return None
        #  过滤掉 ip地址不加任何后缀 （http://127.0.0.1:8000/ 不需要登录验证）
        if path == '/':
            return None
        # 用正则匹配来校验地址
        #  包括静态文件在内的所有文件路径也要排除验证
        not_check = ['/user/login/', '/user/register/', '/goods/.*/', '/cart/.*/', '/media/.*/', '/static/.*/']
        for check_path in not_check:
            if re.match(check_path, path):
                return None
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))


class SessionDbMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 同步session中的商品信息和数据库中购物车表的商品信息
        # 1. 判断用户是否登录，登录才做数据同步操作
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步数据
            #  判断session中的商品是否存在于数据库，存在就更新数据，不存在就创建，并且把数据库数据更新到session中、
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    # se_goods 为：[goods_id, num, is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id, goods_id=se_goods[0]).first()
                    if cart:
                        # 更新数据库中商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建商品信息
                        ShoppingCart.objects.create(user_id=user_id, goods_id=se_goods[0],
                                                    nums=se_goods[1], is_select=se_goods[2])
            # 同步数据库中的数据到session中
            db_cart = ShoppingCart.objects.filter(user_id=user_id)
            #  组装数据结构到session中
            if db_cart:
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_cart]
                request.session['goods'] = new_session_goods
        return response


class ReadRecodeMiddleware(MiddlewareMixin):
    """在访问商品详情页面时，响应页面之前有序的记录查看的商品id值（实现最近浏览功能）"""
    def process_response(self, request, response):
        path = request.path
        #  将请求地址与商品详情页面url匹配
        re_list = re.findall(r'/goods/detail/(\d+)/', path)
        #  如果第一次访问，给session添加列表属性为空，如果不是第一次则获取
        read_list = request.session.get('read_list', [])
        #  判断请求的地址是否是商品详情页面
        if re_list != []:
            #  在访问的地址中获取商品的id值
            goods_id = int(re_list[0])
            #  判断用户有没有访问过商品详情页面
            if read_list != []:
                #   访问过商品详情，如果之前访问过相同的商品，删除之前相同的id
                for id in read_list[::]:
                    if goods_id == id:
                        read_list.remove(id)
                #  将访问的商品id插入到列表的第一个元素之前
                read_list.insert(0, goods_id)
                #  刷新session中列表的值
                request.session['read_list'] = read_list
                return response
            #  用户没有访问过商品详情页面
            else:
                #  直接添加第一个商品详情页面
                read_list.append(goods_id)
                #  刷新商品详情列表
                request.session['read_list'] = read_list
                return response
        return response