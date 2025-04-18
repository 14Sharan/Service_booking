from django import template
register = template.Library()
from accounts.constants import *
from django.db.models import Q
from accounts.models import *

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_.pop('click', None)
    if field == 'spage':
        dict_['click'] = 'other'
    dict_[field] = value
    return dict_.urlencode()
	

@register.filter(name='service_provider_count')
def service_provider_count(key):
    if key == 1:
	    return User.objects.filter(user_status=ACTIVE,role_id=SERVICE_PROVIDER).count()
    elif key == 2:
        return User.objects.filter(user_status=INACTIVE,role_id=SERVICE_PROVIDER).count()
    elif key == 3:
        return User.objects.filter(user_status=DELETED,role_id=SERVICE_PROVIDER).count()
    else:
        return User.objects.filter(role_id=SERVICE_PROVIDER).count()
@register.filter(name='users_count')
def users_count(key):
    if key == 1:
	    return User.objects.filter(user_status=ACTIVE,role_id=USER).count()
    elif key == 2:
        return User.objects.filter(user_status=INACTIVE,role_id=USER).count()
    elif key == 3:
        return User.objects.filter(user_status=DELETED,role_id=USER).count()
    else:
        return User.objects.filter(role_id=USER).count()


@register.filter(name='split_email')
def split_email(email):
    return email.split('@')[0]


# facebook_url check