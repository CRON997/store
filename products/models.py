from django.db import models

from users.models import User


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

    def __str__(self):
        return f"{self. name}|{self.category.name}"


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
