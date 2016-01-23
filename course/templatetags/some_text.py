from django import template

from course.models.desc import Description

register = template.Library()


@register.simple_tag
def insert_text(name):
    """
    Insert a description from the database.

    :param name: name of the description.
    :return: String
    """
    return Description.objects.get(name=name).desc