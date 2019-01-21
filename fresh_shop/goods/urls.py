from django.urls import path

from goods import views
urlpatterns = [
    path('index/', views.index, name='index'),
    #  点击具体商品，显示详情
    path('detail/<int:id>/', views.detail, name='detail'),
    path('list/<int:id>/<int:page>/', views.list, name='list'),
    path('search/', views.search, name='search'),
]