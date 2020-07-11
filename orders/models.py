from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class categories (models.Model):
    name=models.CharField(max_length=64)

class regularPizza (models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class sicilianPizza (models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class toppings (models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class subs (models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class pasta (models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class dinnerPlatters (models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4,decimal_places=2)
    large=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} -{self.large}"

class salad (models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

class order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.IntegerField(default=0)
    toppingAllowance = models.IntegerField(default=0)
    status= models.CharField(max_length=64,default='initiated')

    def __str__(self):
        return (f'Order #{self.order_number} placed by {self.user}: toppingAllowance={self.toppingAllowance} : status={self.status}')

class order_items (models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    category = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return (f'#{self.order}: {self.category} - {self.name} - ${self.price}')
