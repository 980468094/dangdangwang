# 定义购物车项目类，用来存放购物车中数的名称和数量
from mainapp.models import Booklist


class CartItem():
    def __init__(self,book,amount):
        self.amount = amount
        self.book = book
        # 选做
        # self.status = 1


# 定义购物车类，用来更新购物车中的各种需求
class Cart():
    def __init__(self):
        self.save_price = 0
        self.total_price = 0
        self.cartitem = []
    # 计算购物车中商品的节省金额一级总金额
    def sums(self):
        self.save_price = 0
        self.total_price = 0
        for i in self.cartitem:
            self.total_price += i.book.paper * i.amount
            self.save_price += (i.book.market_price - i.book.paper) * i.amount
    # 向购物车中添加书籍
    def add_book(self,bookid,num):
        for i in self.cartitem:
            if i.book.id == int(bookid):
                i.amount += int(num)
                self.sums()
                return
        book = Booklist.objects.filter(id = bookid)[0]
        self.cartitem.append(CartItem(book,int(num)))
        self.sums()

    # 修改购物车的商品信息
    def modify_cart(self,bookid,amount):
        for i in self.cartitem:
            if i.book.id == int(bookid):
                i.amount = int(amount)
            self.sums()

    # 删除购物车
    def delete_cart(self,bookid):
        for i in self.cartitem:
            if i.book.id == int(bookid):
                self.cartitem.remove(i)
        self.sums()
