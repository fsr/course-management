import bleach


# In bleach 6.x, ALLOWED_TAGS is a frozenset, so we need to use set operations
DESCR_ALLOWED_TAGS = set(bleach.ALLOWED_TAGS) | {'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'p', 'img'}
USER_DESCR_ALLOWED_TAGS = set(bleach.ALLOWED_TAGS) | {'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'p'}


def clean_for_user_description(html):
    """
    Removes dangerous tags, including h1.
    """
    return bleach.clean(html, tags=USER_DESCR_ALLOWED_TAGS, strip=True)


def clean_for_description(html):
    """
    Removes dangerous tags.
    """
    # Copy ALLOWED_ATTRIBUTES to avoid modifying the original
    allowed_attrs = dict(bleach.ALLOWED_ATTRIBUTES)
    allowed_attrs['img'] = ['src']
    return bleach.clean(html, tags=DESCR_ALLOWED_TAGS, attributes=allowed_attrs, strip=True)


def clean_all(html):
    """
    Removes *all* html tags.
    """
    return bleach.clean(html, tags=[], attributes=[], strip=True)
