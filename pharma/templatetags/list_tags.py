# your_app/templatetags/list_tags.py
from django import template

register = template.Library()

@register.filter
def unique(value):
    """Removes duplicates while preserving order."""
    result = []
    seen = set()
    for item in value:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
