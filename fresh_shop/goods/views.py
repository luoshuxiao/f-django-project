from django.core.paginator import Paginator
from django.shortcuts import render

from fresh_shop.settings import LIST_NUMBER
from goods.models import Goods, GoodsCategory


def index(request):
    """
    访问首页
    :param request:
    :return:
    """
    if request.method == 'GET':
        #  从数据库查数据返回数据到页面
        # 数据返回方式一：
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data =[category, goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html', {'result': result, 'category_type': category_type})


def detail(request, id):
    if request.method == 'GET':
        #  返回商品详情
        goods = Goods.objects.filter(id=id).first()
        category = goods.category
        return render(request, 'detail.html', {'category': category, 'goods': goods})


def list(request, id, page):
    if request.method == 'GET':
        category = GoodsCategory.objects.filter(id=id)[0]
        goods = category.goods_set.all()
        p_goods = Paginator(goods, LIST_NUMBER).page(page)
        return render(request, 'list.html',{'category': category, 'page_goods': p_goods})


def search(request):
    if request.method == 'GET':
        words = request.GET.get('words')
        #  判断搜索框是否提交了内容
        if words:
            category_g = GoodsCategory.objects.filter(category_name__contains=words).first()
            search_goods = Goods.objects.filter(name__contains=words)
            # 按照类别匹配搜索
            if category_g:
                goods = category_g.goods_set.all()
                s_goods = Paginator(goods,LIST_NUMBER).page(1)
                category = f'关于<{category_g.category_name}>的搜索结果'
                return render(request, 'search.html', {'search_result': category, 'page_goods': s_goods})
            # 按照商品名字匹配搜索
            if search_goods.first():
                s_goods = Paginator(search_goods, LIST_NUMBER).page(1)
                category = f'关于<{words}>的搜索结果'
                return render(request, 'search.html', {'search_result': category, 'page_goods': s_goods})
            # 类别和商品都不能匹配到
            if not search_goods.first() and not category_g:
                category = f'无法找到关于<{words}>的商品'
                return render(request, 'search.html', {'search_result': category})
        #  没有输入搜索内容
        category = f'请输入搜索内容'
        return render(request, 'search.html', {'search_result': category})