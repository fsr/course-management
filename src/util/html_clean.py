import bleach


DESCR_ALLOWED_TAGS = bleach.ALLOWED_TAGS + ['h5', 'h6']


def clean_for_description(html):
    return bleach.clean(html, allowed_tags=DESCR_ALLOWED_TAGS, strip=True)
