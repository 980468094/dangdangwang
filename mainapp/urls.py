from django.urls import path
from mainapp import views

app_name = 'mainapp'

urlpatterns = [
    # 主页面模块
    path('main/',views.main,name = 'main'),
    path('detail/',views.detail,name = 'detail'),

    # 图书列表模块
    path('bookList/', views.bookList, name='bookList'),

    # 购物车模块
    path('shopCar/', views.shopCar, name='shopCar'),
    path('address/', views.address, name='address'),
    path('orderOk/', views.orderOk, name='orderOk'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('registerOk/', views.registerOk, name='registerOk'),
    path('isEmail/', views.isEmail, name='isEmail'),
    path('pwd/', views.pwd, name='pwd'),
    path('repwd/', views.repwd, name='repwd'),
    path('check/', views.check, name='check'),
    path('checkcode/', views.checkcode, name='checkcode'),
    path('loginre/', views.loginre, name='loginre'),
    path('main1/', views.main1, name='main1'),
    path('add/', views.add, name='add'),
    path('display_car/', views.display_car, name='display_car'),
    path('del_book_info/', views.del_book_info, name='del_book_info'),
    path('change_goodsNum/', views.change_goodsNum, name='change_goodsNum'),
    path('register_success/', views.register_success, name='register_success'),
    path('name/', views.name, name='name'),
    path('choice_address/', views.choice_address, name='choice_address'),
    # 邮箱模块
    # path('send_email1/', views.send_email, name='send_email'),

]