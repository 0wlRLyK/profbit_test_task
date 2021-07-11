import datetime

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Sum, DecimalField, Count
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from orders.forms import DatetimeRangeForm, MaxItemsForm
from orders.models import Order, OrderItem


class OrdersByTime(ListView, FormMixin):
    template_name = "orders_by_time.html"
    context_object_name = "orders"
    form_class = DatetimeRangeForm

    def get_queryset(self):
        try:
            from_date = datetime.datetime.strptime(self.request.GET.get("from_date", "01.01.2018 09:00"),
                                                   "%d.%m.%Y %H:%M")
            to_date = datetime.datetime.strptime(self.request.GET.get("to_date", "01.01.2018 10:00"), "%d.%m.%Y %H:%M")
        except ValueError:
            from_date = datetime.datetime(day=1, month=1, year=2018, hour=9)
            to_date = datetime.datetime(day=1, month=1, year=2018, hour=10)
        return Order.objects.filter(
            created_date__gte=from_date, created_date__lte=to_date
        ).annotate(
            order_sum=Sum(
                F("order_items__product_price") * F("order_items__amount"),
                output_field=DecimalField()
            )
        ).prefetch_related("order_items")


class OrderItemsMostPurchased(ListView, FormMixin):
    template_name = "order_items_purchased.html"
    context_object_name = "order_items"
    form_class = MaxItemsForm

    def get_queryset(self):
        try:
            from_date = datetime.datetime.strptime(self.request.GET.get("from_date", "01.01.2018 09:00"),
                                                   "%d.%m.%Y %H:%M")
            to_date = datetime.datetime.strptime(self.request.GET.get("to_date", "01.01.2018 10:00"), "%d.%m.%Y %H:%M")
            max_items = int(self.request.GET.get("max_items", 20))
        except ValueError:
            from_date = datetime.datetime(day=1, month=1, year=2018, hour=9)
            to_date = datetime.datetime(day=1, month=1, year=2018, hour=10)
            max_items = 20
        top_items = OrderItem.objects.values_list('product_name', flat=True)
        filtered_items = OrderItem.objects.filter(
            product_name__in=list(top_items), order__created_date__gte=from_date,
            order__created_date__lte=to_date
        ).select_related("order").values("product_name").annotate(
            total_sold=Sum('amount'),
            length=Count('order__number') + 1,
            product_prices=ArrayAgg("product_price"),
            numbers=ArrayAgg('order__number'),
            dates=ArrayAgg('order__created_date'),
        ).values(
            "product_name", "length", "total_sold", "numbers", "product_prices", "dates"
        ).order_by('-total_sold')[:max_items]
        return filtered_items
