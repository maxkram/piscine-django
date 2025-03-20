from django import template

register = template.Library()

@register.filter
def join_with(value, delimiter):
    if isinstance(value, (list, tuple)):
        return delimiter.join(str(item) for item in value)
    return value