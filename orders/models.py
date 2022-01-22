from django.db import models

from utilities.constants import CATEGORIES, STATUSES
from vauth.models import User
from wallet.models import Transaction

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=2, choices=CATEGORIES)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=CATEGORIES)
    items = models.ManyToManyField(Item)

    @property
    def total_price(self):
        return self.items.all().aggregate(models.Sum("price"))


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    transaction = models.ForeignKey(
        Transaction, on_delete=models.PROTECT, null=True, blank=True
    )
    status = models.CharField(max_length=2, choices=STATUSES, default="P")
    vendor = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="vendor")

    @property
    def reference(self):
        return self.transaction.reference if self.transaction else None

    @property
    def paid(self):
        return self.transaction == True

    @property
    def total_order_price(self):
        return self.orderitem_set.all().aggregate(
            sum=models.Sum(models.F("ordered_price") * models.F("quantity"))
        )["sum"]


class OrderItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True)
    ordered_price = models.FloatField()
    quantity = models.IntegerField(default=1)
