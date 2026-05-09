from datetime import date

from django import template

register = template.Library()


@register.simple_tag
def curr_year():
    return date.today().year
