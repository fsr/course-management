from django import template
from django.conf import settings

register = template.Library()

SITE_KEY = settings.RE_CAPTCHA_SITE_KEY

@register.inclusion_tag('tags/re-captcha.html')
def captcha_tag():
    return {
        'key': SITE_KEY
    }
