from django import template
from course.models.subject import Subject

register = template.Library()

@register.inclusion_tag('active-subjects.html')
def show_active_subjects():
    return { 'active_subjects' : Subject.get_active() }
