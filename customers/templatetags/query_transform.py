# customers/templatetags/query_transform.py
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the current query string with updated parameters.
    
    Usage in template:
      {% query_transform page=page_obj.previous_page_number %}
    """
    # Copy existing GET parameters
    query = context["request"].GET.copy()
    # Update with new values (or override)
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()
