from django.urls import path

from orders.views import OrdersByTime, OrderItemsMostPurchased

app_name = "orders"
urlpatterns = [
    path("orders/", OrdersByTime.as_view(), name="by_time"),
    path("top_order_items/", OrderItemsMostPurchased.as_view(), name="most_purchased")
]
