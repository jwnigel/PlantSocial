from django import template
import random

register = template.Library()

@register.filter
def random_shuffle(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items