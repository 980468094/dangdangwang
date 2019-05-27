# encoding:utf-8
from django.test import TestCase

# Create your tests here.

# python manage.py inspectdb  作用：根据数据库建立django模型（只生成）

# python manage.py inspectdb > mainapp/models.py  作用：将模型导入我的app
# Booklist.objects.create(book_name = '',author = '',market_price = '',publish_time = datetime.datetime.now(),publish = '',sales = '',edition = '',font_num = '',page = '',print = '',format = '',print_num = '',paper = '',ISBN = '',package = '',author_intro = '',content = '',recommend = '',inventory = '',list = '',book_pic = '',two_category = '',two_id = '')
from mainapp.models import Booklist
import datetime



