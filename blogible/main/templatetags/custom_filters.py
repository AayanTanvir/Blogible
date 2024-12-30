from django import template

register = template.Library()

@register.filter
def format_number(value):
    if isinstance(value, int) or isinstance(value, float):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}m"
        elif value >= 1_000:
            return f"{value / 1_000:.1f}k"
        else:
            return str(value)
    else:
        return value