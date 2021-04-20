from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    '''
    Товары.
    '''
    name = models.CharField(max_length=60)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}. Цена {self.price}.'


class Cart(models.Model):
    '''
    Корзина.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        entrys = Entry.objects.filter(cart=self)
        return f'Корзина {self.user.username}. {len(entrys)} товаров.'


class Entry(models.Model):
    '''
    Элементы корзины.
    '''
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f'Элемент корзины {self.cart.user.username}. id {self.id}'


class Order(models.Model):
    '''
    Заказ.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    sum = models.IntegerField(default=0)

    def cart_to_order(self, cart):
        entrys = Entry.objects.filter(cart=cart)
        sum_ = 0
        for entry in entrys:
            order_item, _ = OrderItem.objects.get_or_create(product=entry.product, order=self)
            sum_ += entry.product.price
            entry.delete()
        self.sum = sum_
        self.save()

class OrderItem(models.Model):
    '''
    Элементы заказа.
    '''
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)