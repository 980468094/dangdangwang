import random,string,re,datetime

# import send_email as send_email
from django.db import transaction
from django.http import JsonResponse
from mainapp.post_email import hash_code
from mainapp.cart import Cart
from mainapp.captcha.image import ImageCaptcha
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
# Create your views here.
from mainapp.models import BookClassify, Booklist, Users, Address, OrderList, Confirm_string


# 模块1 主页面和详情页
# 显示分类信息
def main(request):
    index = BookClassify.objects.filter(parent_id=0)
    second = BookClassify.objects.filter(parent_id__gt=0)
    new = Booklist.objects.all().order_by('-publish_time')
    hot = Booklist.objects.all().order_by('-sales')
    name = request.session.get('name')
    return render(request,'index.html',{'index':index,'second':second,'new':new,'hot':hot,'name':name})


def main1(request):
    index = BookClassify.objects.filter(parent_id=0)
    second = BookClassify.objects.filter(parent_id__gt=0)
    new = Booklist.objects.all().order_by('-publish_time')
    hot = Booklist.objects.all().order_by('-sales')
    del request.session['name']
    return render(request,'index.html',{'index':index,'second':second,'new':new,'hot':hot})


# 详情页
def detail(request):
    id = request.GET.get('id')
    deta = Booklist.objects.filter(id=id).values()[0]
    aa = deta['two_id']
    # 一级分类
    bb = BookClassify.objects.filter(id = aa).values()[0]
    cc = bb['parent_id']
    # 二级分类
    dd = BookClassify.objects.filter(id=cc).values()[0]
    name = request.session.get('name')
    # print(name)
    discount = round(deta['paper']/deta['market_price']*10,2)
    # print(round(discount,2))
    return render(request,'Book details.html',{'deta':deta,'dd':dd,'name':name,'discount':discount,'id':id})


# 模块2：图书列表
# 图书列表
def bookList(request):
    # 对列表页面进行分类
    index = BookClassify.objects.filter(parent_id=0)
    second = BookClassify.objects.filter(parent_id__gt=0)
    # 判断用户点击的是几级分类，并显示当前分类下的图书
    id1 = request.GET.get('id1')
    id2 = request.GET.get('id2')
    # print(id2)
    # 获取以及分类名称
    name = BookClassify.objects.filter(id=id1).values()[0]
    name1 = BookClassify.objects.filter(parent_id=id1).values()[0]
    '''
    判断用户点击的是以及分类还是二级分类,当点击的是一级分类二级分类获取的应该是none值
    获取以及分类下所有的model,并将其储存在一个列表中
    '''
    l = []
    if id2 == None:
        id_2 = BookClassify.objects.filter(parent_id=id1).values()
        for id in id_2:
            l.append(id['id'])
        # 返回id在这个列表中的query
        info = Booklist.objects.filter(two_id__in=l)   #当时不会这个语法!!!!!\
        # print(l,info)
    elif id2 =='None':
        id_2 = BookClassify.objects.filter(parent_id=id1).values()
        for id in id_2:
            l.append(id['id'])
        info = Booklist.objects.filter(two_id__in=l)  # 当时不会这个语法!!!!!\
    else:
        info = Booklist.objects.filter(two_id=id2)
        # print(info)
    # 对筛选出来的数据进行分页
    number = request.GET.get('number')
    bb = info.count()
    pagtor = Paginator(info,per_page=3)
    name2 = request.session.get('name')
    if not number or int(number)>pagtor.num_pages:
        number = 1
        page = pagtor.page(number)
        all_page = pagtor.num_pages
        return render(request,'booklist.html',{
            'name':name,
            'name1':name1,
            'name2':name2,
            'bb':bb,
            'page':page,
            'index':index,
            'second':second,
            'number':number,
            'id1':id1,
            'id2':id2,
            'all_page':all_page,
        })
    else:
        page = pagtor.page(number)
        all_page = pagtor.num_pages
        return render(request, 'booklist.html', {
            'name': name,
            'name1': name1,
            'name2': name2,
            'bb': bb,
            'page': page,
            'index': index,
            'second': second,
            'number': number,
            'id1': id1,
            'id2': id2,
            'all_page': all_page,
        })

# 模块3：在购物车添加商品，减少物品、删除物品等
# 购物车页面
def shopCar(request):
    name = request.session.get('name')
    return render(request,'car.html',{'name':name})

# 添加至购物车
def add(request):
    try:
        with transaction.atomic():
            bookid = request.GET.get('bookid')  # 获取书的id
            num = request.GET.get('num')
            # 刚开始此处飘黄是因为和下面session重复调用了
            cart = request.session.get('cart')
            # print(bookid,num)
            if cart is None:
                cart = Cart()
                cart.add_book(bookid,num)
                request.session['cart'] = cart
            else:
                cart.add_book(bookid,num)
                request.session['cart'] = cart
            return JsonResponse({'fail':'添加成功'},safe=False)
    except Exception as e:
        return JsonResponse({'fail':'添加失败'},safe=False)


# 将图书展示在购物车中
def display_car(request):
    info = request.session.get('cart')
    if info:
        goods_info = info.cartitem
        total_price = info.total_price
        save_price = info.save_price
        all_num = 0
        name = request.session.get('name')
        for i in goods_info:
            all_num += i.amount
        return render(request, 'car.html',
                      {'goods_info': goods_info, 'total_price': total_price, 'save_price': save_price,
                       'all_num': all_num, 'name': name})
    else:
        return render(request,'car.html')

# 删除购物车中的图书
def del_book_info(request):
    bookid = request.GET.get('bookid')
    info = request.session.get('cart')
    info.delete_cart(bookid)
    request.session['cart'] = info
    return redirect('mainapp:display_car')

# 修改购物车中商品数量
def change_goodsNum(request):
    cart = request.session.get('cart')
    bookid = request.GET.get('bookid')
    amount = request.GET.get('amount')
    cart.modify_cart(bookid,amount)
    request.session['cart'] = cart
    total_price = cart.total_price
    save_price = cart.save_price
    all_num = 0
    for i in cart.cartitem:
        all_num += i.amount
        if int(i.book.id) == int(bookid):
            dangdangprice = i.book.paper
            return render(request, 'car.html',
                          {'goods_info': cart.cartitem, 'total_price': total_price, 'save_price': save_price,'all_num': all_num
                           })

# 模块4：订单模块
# 点击结算之后判断用户是否登录
def address(request):
    flag = request.GET.get('flag')
    name = request.session.get('name')
    '''
    如果name有返回值说明用户是登录状态,
    然后将session中的数据传到页面
    '''
    if name:
        id = request.session.get('id')
        cart = request.session.get('cart')
        goods_info = cart.cartitem
        address_info = Address.objects.filter(user_id=id).values()
        total_price = cart.total_price
        # sub_price = (i.amount)*(i.book.paper)
        return render(request,'indent.html',{'goods_info':goods_info,'address_info':address_info,'total_price':total_price,'name':name})
    #否则跳转到登录页面
    else:
        return render(request,'login.html',{'flag':flag})


# 订单提交完成
def orderOk(request):
    # 获取用户选的是新地址还是旧地址
    id = request.session.get('id')
    aa = Address.objects.filter(user_id=id)
    if aa:
        # print('qqqqq')
        pass
    else:
        # if aa.name_address != request.GET.get('receive'):
        # 保存地址
        name_address = request.GET.get('receive')
        address_address = request.GET.get('detail_address')
        post_num = request.GET.get('post_num')
        telephone_num = request.GET.get('telephone')
        phone_num = request.GET.get('phone')
        user_id = id
        # print(name_address,address_address,post_num,telephone_num,phone_num,user_id)
        Address.objects.create(name_address=name_address,address_address=address_address,post_num=post_num,telephone_num=telephone_num,phone_num=phone_num,user_id=user_id)
    # 保存订单
    name = request.session.get('name')
    cart = request.session.get('cart')
    if cart:
        goods_info = cart.cartitem
        # 从a-zA-Z0-9生成指定数量的随机字符：
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        a = 0
        ff = Address.objects.filter(user_id=id)[0]

        for i in goods_info:
            a += 1
            # print(i.book.book_name)
            total_price = cart.total_price
            user_id1 = id
            order_num = i.amount
            sub_price = (i.amount)*(i.book.paper)
            date = datetime.now()
            address_id = ff.address_id
            OrderList.objects.create(total_price=total_price,order_num=order_num,sub_price=sub_price,date=date,user_id=user_id1,address_id=address_id)
        ss = Address.objects.filter(user_id=id).values()[0]
        del request.session['cart']
        return render(request, 'indent ok.html',
                      {'name_address': ss['name_address'], 'ran_str': ran_str, 'total_price': cart.total_price,
                       'order_num': a, 'name': name})
    else:
        return redirect('mainapp:shopCar')

# 登录界面
def login(request):
    return render(request,'login.html')

# 接收登录页面信息验证
def loginre(request):
    flag = request.GET.get('flag')
    email = request.POST.get('txtUsername')  # 获取用户信息
    password = request.POST.get('txtPassword')
    checkcode = request.POST.get('checkcode')
    result = Users.objects.filter(email=email, password=password,has_confirm=1)
    if result and checkcode.upper() == request.session['code'].upper():  # 返回到主页面
        request.session['name'] = result.values()[0]['name']
        request.session['id'] = result.values()[0]['id']
        if flag:
            return redirect('mainapp:address')
        else:
            res = redirect('mainapp:main')
        res.set_cookie('username', email.encode('utf-8').decode('latin-1'), max_age=7 * 24 * 3600)  # 将信息储存在浏览器中
        res.set_cookie('password', password.encode('utf-8').decode('latin-1'), max_age=7 * 24 * 3600)
        return res

    else:
        return redirect('mainapp:login')


# 注册界面
def register(request):
    flag = request.GET.get('flag')
    return render(request,'register.html',{'flag':flag})



# 验证用户名是否存在
def isEmail(request):
    email = request.GET.get('email')
    if email == '':
        return HttpResponse('空')
    else:
        check_email = re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*|^1\d{10}',email)
        if check_email:
            return HttpResponse('正确')
        return HttpResponse('邮箱格式有误')

# 验证用户名格式
def name(request):
    pwd1 = request.GET.get('name')
    if pwd1 == '':
        return HttpResponse('空')
    else:
        return HttpResponse('正确')


# 验证密码格式
def pwd(request):
    pwd1 = request.GET.get('pwd1')
    if pwd1 == '':
        return HttpResponse('空')
    elif len(pwd1)>20 or len(pwd1)<6:
        return HttpResponse('长度')
    else:
        check_pwd = re.match(r'^\w{6,20}$',pwd1)
        # print(check_pwd)
        if check_pwd:
            return HttpResponse('正确')
        return HttpResponse('密码格式有误')

# 密码一致性验证
def repwd(request):
    pwd1 = request.GET.get('pwd1')
    pwd2 = request.GET.get('pwd2')
    if pwd1 == pwd2 and pwd1 != '' and 5<len(pwd1)<21:
        return HttpResponse('正确')
    return HttpResponse('密码格式有误')

# 生成验证码
def check(request):
    #此处可以添加一个字体
    #构造图片验证码对象
    image = ImageCaptcha()
    code = random.sample(string.ascii_letters+string.ascii_uppercase+string.digits,2)
    re_code = ''.join(code)   #将code列表转成字符串
    request.session['code'] = re_code
    # 将字符串生成图片
    checkcode = image.generate(re_code)
    return HttpResponse(checkcode,'image/jpg')


# 判断验证码是否一致
def checkcode(request):
    check = request.GET.get('check')
    if check.upper() == request.session['code'].upper():
        return HttpResponse('两相同')
    else:
        return HttpResponse('不相同')


# 二次验证用户注册信息是否合法，不合法不能跳转页面
def registerOk(request):
    email = request.GET.get('txt_username')
    name = request.GET.get('txt_name')
    password = request.GET.get('txt_password')
    passwordre = request.GET.get('txt_repassword')
    number = request.GET.get('txt_vcode')
    info = Users.objects.filter(email=email)
    check_email = re.match('\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*|^1\d{10}', email)
    if info != None and check_email == None:
        return HttpResponse('邮箱格式有误')
    elif password != passwordre or 20<len(password) or len(password)<6:  # 如果注册成功，跳转到登录界面
        return HttpResponse('两次密码不一致')
    elif number.upper() != request.session['code'].upper():
        return HttpResponse('验证码有误~')
    else:
        # print(email,name,password)
        Users.objects.create(email=email,name=name,password=password)
        new_user = Users.objects.get(email=email)
        code = make_confirm_string(new_user)
        # print(code)
        send_email1(email,code)
        return HttpResponse('注册成功')

# 跳转到用户注册成功界面
def register_success(request):
    email = request.GET.get('email')
    code = request.GET.get('code')
    hh = Confirm_string.objects.filter(code=code)
    print(hh,code)
    if hh:
        user_info = Users.objects.filter(id=hh[0].user_id)
        print(user_info)
        mm = user_info[0]
        mm.has_confirm = 1
        mm.save()
        request.session['has_confirm'] = 1
        return render(request,'register ok.html',{'email':email})
    else:
        return render(request,'register ok.html',{'email':email})


# 从购物车跳转过来的注册完成后需要返回到填写收货地址页面
def register_address(request):
    return redirect('mainapp:address')

# 选择地址中对应的姓名显示对应的地址信息
def choice_address(request):
    address_id = request.GET.get('address_id')
    # print(address_id)
    address_info = Address.objects.filter(address_id=address_id).values()[0]
    name_address = address_info['name_address']
    address_address = address_info['address_address']
    post_num = address_info['post_num']
    phone_num = address_info['phone_num']
    telephone_num = address_info['telephone_num']
    # print(name_address,address_address,post_num,phone_num,telephone_num)
    return JsonResponse({'name_address':name_address,
                         'address_address':address_address,
                         'post_num':post_num,
                         'phone_num':phone_num,
                         'telephone_num':telephone_num,
                         },safe=False)

#邮箱模块

from datetime import datetime
from mainapp.models import Confirm_string
from dangdangwang.settings import EMAIL_HOST_USER
import hashlib

import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'dangdangwang.settings'

# 生成邮箱验证码
def make_confirm_string(new_user):
    now = datetime.now().strftime('%Y-%m-%d %H:%H:%S')
    code = hash_code(new_user.name,now)
    Confirm_string.objects.create(code=code,user=new_user)
    return code


# 发送邮件函数
def send_email1(email,code,):
        # subject, from_email, to = '来自的测试邮件', '18500230996@sina.cn', ['maoxinyu925@163.com','18640964660@163.com']
        subject = '注册验证码'
        text_content = '欢迎访问帅气小伙的购物网站，请点击下面链接进行邮箱验证。'
        html_content = '<p>感谢注册<a href="http://{}/mainapp/register_success/?code={}&email={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1:8000',code,email)
        # 发送邮件所需要的方法及需要的参数
        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
        # 发送HTML文本的内容
        msg.attach_alternative(html_content, "text/html")
        msg.send()