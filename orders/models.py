from django.db import models


class Order(models.Model):
    number = models.IntegerField()
    created_date = models.DateTimeField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=7, decimal_places=2)
    amount = models.IntegerField()
