from django.urls import path

from order import views

urlpatterns = [
    # 结算功能
    path('place_order/', views.place_order, name='place_order'),
    #  创建功能
    path('order/', views.order, name='order')
]