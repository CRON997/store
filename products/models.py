from locale import currency

from django.db import models
import stripe
from users.models import User
from django.conf import settings

stripe.api_key=settings.STRIPE_SECRET_KEY

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self. name}"

    class Meta:
        verbose_name_plural = 'Product Categories'


class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=64, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    characteristics = models.JSONField(default=dict, blank=True)
    stripe_product_price_id = models.CharField(max_length=128,null=True,blank=True)


    def __str__(self):
        return f"{self. name}|{self.category.name}"


    def save(self,force_insert=False,force_update=False,using=None,update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price =self.create_stripe_product_price()
            self.stripe_product_price_id =stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=using, update_fields=update_fields)

    def create_stripe_product_price(self):
        stripe_product =stripe.Product.create(name=self.name)
        stripe_product_price= stripe.Price.create(product=stripe_product['id'],unit_amount= round(self.price *100),currency='uah')
        return stripe_product_price


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket for {self.user.username} | Product {self.product.name}"

    def sum(self):
        res = self.quantity * self.product.price
        return res

    def de_json(self):
        basket_item ={
            'product_name':self.product.name,
            'quantity':self.quantity,
            'price':float(self.product.price),
            'sum':float(self.sum())
        }
        return basket_item