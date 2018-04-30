from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def safe_referrer(request, default):
    """
    Takes the request and a default URL. Returns HTTP_REFERER if it's safe
    to use and set, and the default URL otherwise.

    The default URL can be a model with get_absolute_url defined, a urlname
    or a regular URL
    """
    referrer = request.META.get('HTTP_REFERER')
    if referrer and is_safe_url(referrer, request.get_host()):
        return referrer
    if default:
        # Try to resolve. Can take a model instance, Django URL name or URL.
        return resolve_url(default)
    else:
        # Allow passing in '' and None as default
        return default


def check_user_groups(user, group_list):
    """
    Check if given user is in group_list.
    Return boolean
    """
    if not isinstance(user, UserModel) and isinstance(group_list, list):
        return False
    else:
        if not [i for i in group_list if i in [x.name for x in user.groups.all()]]:
            return False

        return True
