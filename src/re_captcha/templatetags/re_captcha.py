from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('tags/re-captcha.html')
def captcha_tag():
    return {
        'key': settings.RE_CAPTCHA_SITE_KEY
    }
