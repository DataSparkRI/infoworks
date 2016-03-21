from django import template
from front_page.models import Config

register = template.Library()

@register.filter(name='get_config')
def get_config(config_name):
    try:
        return Config.objects.get(name=config_name).value
    except:
        return None
