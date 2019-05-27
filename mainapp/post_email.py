from datetime import datetime
from mainapp.models import Confirm_string
from dangdangwang.settings import EMAIL_HOST_USER
import hashlib

import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'send_email.settings'

def send_email(email,code):
        # subject, from_email, to = '来自的测试邮件', '18500230996@sina.cn', ['maoxinyu925@163.com','18640964660@163.com']
        subject = '撒吗'
        text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
        html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '.format('127.0.0.1',code)
        # 发送邮件所需要的方法及需要的参数
        msg = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [email])
        # 发送HTML文本的内容
        msg.attach_alternative(html_content, "text/html")
        msg.send()




def hash_code(name, now):
    h = hashlib.md5()
    name += now
    h.update(name.encode())
    return h.hexdigest()

# def make_confirm_string(new_user):
#     now = datetime.now().strftime('%Y-%m-%d %H:%H:%S')
#     code = hash_code(new_user.name,now)
#     Confirm_string.objects.create(code=code,user=new_user)