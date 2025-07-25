from django.db import models

from products.models import Basket
from users.views import User

class Order(models.Model):
    CREATED= 0
    PAID= 1
    ON_WAY= 2
    DELIVERED= 3
    STATUES=((CREATED,'Conceived'),(PAID,'Payed'),(ON_WAY,'En route'),(DELIVERED,'Delivered'))

    first_name=models.CharField(max_length=64)
    last_name=models.CharField(max_length=64)
    email=models.EmailField(max_length=256)
    address=models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status =models.SmallIntegerField(default=CREATED,choices=STATUES)
    initiator = models.ForeignKey(to=User,on_delete=models.CASCADE)

    def __str__(self):
        return f"Order #{self.id}.{self.first_name} - {self.last_name}"

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.initiator)

        # Обновляем количество товаров на складе
        for basket in baskets:
            product = basket.product
            if product.quantity >= basket.quantity:
                product.quantity -= basket.quantity
                product.save()
            else:
                # Обработка случая, когда товара недостаточно на складе
                raise ValueError(f"Недостаточно товара {product.name} на складе. "
                                 f"Доступно: {product.quantity}, запрошено: {basket.quantity}")

        # Сохраняем историю покупок
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(sum(b.sum() for b in baskets))
        }

        # Удаляем корзину после успешной покупки
        baskets.delete()
        self.save()

