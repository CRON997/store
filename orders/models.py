from django.db import models
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