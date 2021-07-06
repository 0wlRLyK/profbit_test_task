import random
import datetime

from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Generates the specified number of orders with a random number of order items (from 1 to 5)'

    def add_arguments(self, parser):
        parser.add_argument('number_of_orders', type=int, help="The number of orders that need to be generated ("
                                                               "positive number)")

    def handle(self, *args, **options):
        num_orders = options["number_of_orders"]
        if num_orders <= 0:
            raise CommandError("The value of argument 'number of orders' must be a positive number")
        tz = timezone.get_current_timezone()
        start_datetime = datetime.datetime.strptime(settings.START_DATETIME, "%m.%d.%Y %H:%M")
        last_id = Order.objects.last().pk
        new_ids = list(range(last_id + 1, last_id + num_orders + 1))

        orders = [
            Order(
                number=el,
                created_date=str(tz.localize(start_datetime + datetime.timedelta(hours=el)))
            )
            for el in range(num_orders)
        ]
        order_items = [
            OrderItem(
                order_id=order_id,
                product_name=f"Товар-{item_name}",
                product_price=random.randint(100, 9999),
                amount=random.randint(1, 10)
            )
            for order_id in new_ids
            for item_name in random.sample(range(1, 100), random.randint(1, 5))
        ]

        Order.objects.bulk_create(orders)
        OrderItem.objects.bulk_create(order_items)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {len(orders)} orders and {len(order_items)}'
                                             f' order items'))
