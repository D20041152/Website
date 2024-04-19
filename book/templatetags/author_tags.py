from django import template

register = template.Library()

@register.simple_tag
def author(authors):
    authors_str = ""
    for elem in authors:
        authors_str += (str(elem) + ", ")
    return authors_str[:-2]
