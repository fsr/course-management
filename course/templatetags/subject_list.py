from django import template

from course.models.subject import Subject

register = template.Library()


@register.inclusion_tag('tags/active-subjects.html')
def show_active_subjects():
    """
    Return a HTML list-thingy of active subjects.

    :return: rendered HTML
    """
    return { 'active_subjects': Subject.get_active() }


@register.inclusion_tag('tags/inactive-subjects.html')
def show_inactive_subjects():
    """
    Return a HTML list-thingy of inactive subjects.

    :return: rendered HTML
    """
    return { 'inactive_subjects': Subject.get_inactive() }

@register.inclusion_tag('tags/visible-subjects.html')
def show_visible_subjects():
    """
    Return a HTML list-thingy of visible subjects.

    :return: rendered HTML
    """
    return { 'visible_subjects': Subject.get_visible() }


@register.inclusion_tag('tags/invisible-subjects.html')
def show_invisible_subjects():
    """
    Return a HTML list-thingy of invisible subjects.

    :return: rendered HTML
    """
    return { 'invisible_subjects': Subject.get_invisible() }
