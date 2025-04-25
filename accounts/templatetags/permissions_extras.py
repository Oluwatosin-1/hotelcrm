from django import template

register = template.Library()


@register.filter
def has_perm(user, perm):
    """
    Usage:
      {% if request.user|has_perm:"reports.change_report" %}
    """
    try:
        return user.has_perm(perm)
    except Exception:
        return False
