from django import template

from course.models.subject import Subject

register = template.Library()


@register.inclusion_tag('tags/active-subjects.html')
def show_active_subjects():
    """
    Return a HTML list-thingy of active subjects.

    :return: rendered HTML
    """
    return { 'active_subjects' : Subject.get_active() }
