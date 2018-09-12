import re


def remove_html_tags(text):
    """Remove html tags from a string"""
    # todo: rewrite that crap
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)
