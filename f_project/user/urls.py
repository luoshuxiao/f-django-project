from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user_center_info/', views.user_center_info, name='user_center_info'),
    path('user_center_order/', views.user_center_order, name='user_center_order'),
    path('user_center_site/', views.user_center_site, name='user_center_site'),
    path('logout/', views.logout, name='logout'),
]