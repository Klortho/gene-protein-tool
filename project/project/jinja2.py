from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
import jinja2

from jinja2 import Environment

@jinja2.contextfunction
def get_context(c):
    return c

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'context': get_context,
    })
    return env

