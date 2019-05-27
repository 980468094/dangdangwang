# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    name_address = models.CharField(max_length=60, blank=True, null=True)
    address_address = models.CharField(max_length=100, blank=True, null=True)
    post_num = models.CharField(max_length=60, blank=True, null=True)
    telephone_num = models.CharField(max_length=60, blank=True, null=True)
    phone_num = models.CharField(max_length=60, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'


class BookClassify(models.Model):
    id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=40, blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_classify'


class BookItem(models.Model):
    id = models.IntegerField(primary_key=True)
    book_name = models.CharField(max_length=40, blank=True, null=True)
    book = models.ForeignKey('Booklist', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_item'


class Booklist(models.Model):
    id = models.BigIntegerField(primary_key=True)
    book_name = models.CharField(max_length=40, blank=True, null=True)
    author = models.CharField(max_length=40, blank=True, null=True)
    market_price = models.CharField(max_length=40, blank=True, null=True)
    publish_time = models.DateField(blank=True, null=True)
    publish = models.CharField(max_length=40, blank=True, null=True)
    sales = models.BigIntegerField(blank=True, null=True)
    edition = models.CharField(max_length=40, blank=True, null=True)
    font_num = models.BigIntegerField(blank=True, null=True)
    page = models.BigIntegerField(blank=True, null=True)
    print = models.DateField(blank=True, null=True)
    format = models.CharField(max_length=40, blank=True, null=True)
    print_num = models.CharField(max_length=40, blank=True, null=True)
    paper = models.CharField(max_length=40, blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=40, blank=True, null=True)  # Field name made lowercase.
    package = models.CharField(max_length=40, blank=True, null=True)
    author_intro = models.CharField(max_length=2000, blank=True, null=True)
    content = models.CharField(max_length=2000, blank=True, null=True)
    recommend = models.CharField(max_length=2000, blank=True, null=True)
    inventory = models.CharField(max_length=40, blank=True, null=True)
    list = models.CharField(max_length=2000, blank=True, null=True)
    book_pic = models.CharField(max_length=2000, blank=True, null=True)
    two_category = models.CharField(max_length=40, blank=True, null=True)
    two = models.ForeignKey(BookClassify, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booklist'


class OrderList(models.Model):
    id = models.BigIntegerField(primary_key=True)
    total_price = models.FloatField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    order_num = models.BigIntegerField()
    sub_price = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    column_8 = models.CharField(db_column='Column_8', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_list'

# 创建用户表
class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    c_time = models.DateTimeField(auto_now_add=True)
    has_confirm = models.BooleanField(default=False,verbose_name='是否确认')
    status = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'users'

# 接受验证码信息
class Confirm_string(models.Model):
    code = models.CharField(max_length=256,verbose_name='用户注册码')
    user = models.ForeignKey('Users',on_delete=models.CASCADE,verbose_name='关联的用户')
    code_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 't_Confirm_string'