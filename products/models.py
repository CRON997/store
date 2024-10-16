from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description =  models.TextField(blank= True)
    

class Product(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='products_images',blank=True)
    description = models.TextField(blank= True)
    short_description = models.CharField(max_length=64,blank=True)
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    quantity= models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
