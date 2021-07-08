import datetime

from django.db.models import F, Sum, DecimalField
from django.views.generic import ListView

from orders.models import Order, OrderItem


class OrdersByTime(ListView):
    template_name = "orders_by_time.html"
    context_object_name = "orders"

    def get_queryset(self):
        try:
            from_date = datetime.datetime.strptime(self.request.GET.get("from", "01.01.2018 09:00"), "%d.%m.%Y %H:%M")
            to_date = datetime.datetime.strptime(self.request.GET.get("to", "01.01.2018 10:00"), "%d.%m.%Y %H:%M")
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


class OrderItemsMostPurchased(ListView):
    template_name = "order_items_purchased.html"
    context_object_name = "order_items"

    def get_queryset(self):
        try:
            from_date = datetime.datetime.strptime(self.request.GET.get("from", "01.01.2018 09:00"), "%d.%m.%Y %H:%M")
            to_date = datetime.datetime.strptime(self.request.GET.get("to", "01.01.2018 10:00"), "%d.%m.%Y %H:%M")
            max_items = int(self.request.GET.get("slice", 20))
        except ValueError:
            from_date = datetime.datetime(day=1, month=1, year=2018, hour=9)
            to_date = datetime.datetime(day=1, month=1, year=2018, hour=10)
            max_items = 20
        top_items = OrderItem.objects.values_list('product_name', flat=True)
        filtered_items = OrderItem.objects.select_related().annotate(
            total_sold=Sum('amount')).order_by('-total_sold').filter(
            product_name__in=list(top_items), order__created_date__gte=from_date,
            order__created_date__lte=to_date)
        result = {}
        for item in filtered_items.iterator():
            if item.product_name not in result:
                result[item.product_name] = [item.total_sold, {
                    'order_number': item.order.number,
                    'product_price': item.product_price,
                    'order_created_date': item.order.created_date,
                }]
            else:
                result[item.product_name][0] += item.total_sold
                result[item.product_name].append(
                    {
                        'order_number': item.order.number,
                        'product_price': item.product_price,
                        'order_created_date': item.order.created_date,
                    }
                )
        result = sorted([{
            "name": k,
            "amount": v.pop(0),
            "details": v,
            "len": len(v) + 1} for k, v in result.items()],
            key=lambda i: i["amount"], reverse=True)[:max_items]

        return result
