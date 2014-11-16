__author__ = 'anthonys'
from django import template


register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
    """
    Adds the CSS classes to the field.

    :param field:
    :param css:
    :return:
    """
    return field.as_widget(attrs={"class": css})
