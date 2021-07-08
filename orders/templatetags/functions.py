from django import template
from django.db import connection

register = template.Library()


@register.simple_tag
def db_queries_counter():
    return len(connection.queries)
