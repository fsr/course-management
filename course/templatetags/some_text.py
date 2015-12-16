from django import template

from course.models.desc import Description

register = template.Library()


@register.simple_tag
def insert_text(name):
    return Description.objects.get(name=name).desc