import bleach


DESCR_ALLOWED_TAGS = bleach.ALLOWED_TAGS + ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'p']
USER_DESCR_ALLOWED_TAGS = bleach.ALLOWED_TAGS + ['h2', 'h3', 'h4', 'h5', 'h6', 'br', 'p']


def clean_for_user_description(html):
    """
    Removes dangerous tags, including h1.
    """
    return bleach.clean(html, tags=USER_DESCR_ALLOWED_TAGS, strip=True)


def clean_for_description(html):
    """
    Removes dangerous tags.
    """
    return bleach.clean(html, tags=DESCR_ALLOWED_TAGS, strip=True)


def clean_all(html):
    """
    Removes *all* html tags.
    """
    return bleach.clean(html, tags=[], styles=[], attributes=[], strip=True)
