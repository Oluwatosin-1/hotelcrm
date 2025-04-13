# accounts/templatetags/extras.py
from django import template

register = template.Library()

@register.filter
def startswith(text, prefix):
    """Return True if *text* starts with *prefix*."""
    return str(text).startswith(prefix)
