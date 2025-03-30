from django import template

register = template.Library()

@register.filter
def zone_range(zones):
    if not zones:
        return ''
    return f'{min(zones)} - {max(zones)}'