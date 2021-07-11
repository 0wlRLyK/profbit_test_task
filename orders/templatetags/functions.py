from django import template
from django.db import connection

register = template.Library()


@register.simple_tag
def db_queries_counter():
    return len(connection.queries)


@register.simple_tag
def zip_orders(order_item):
    return zip(order_item["numbers"], order_item["product_prices"], order_item["dates"])
