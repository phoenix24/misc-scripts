""" 
simple tag returning the application build info.
@author: chaitanya sharma
"""

from django import template

register = template.Library()

@register.filter
def build(revision, release):
    """ this is a tutorial template tag. """
    return "yo! the template seems to work! %s, %s" % (revision, release)

@register.filter(name="mlower")
def mlower(value):
    return value.lower()
#register.filter('mlower', mlower)

@register.filter
def mupper(value):
    return value.upper()
#register.filter('mupper', mupper)

