from django.core.exceptions import PermissionDenied
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.contrib import messages

from ..utils import safe_referrer


class RequestFormKwargsMixin(object):
    """
    CBV mixin which puts the request into the form kwargs.
    Note: Using this mixin requires you to pop the `request` kwarg
    out of the dict in the super of your form's `__init__`.
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'request'):
            # Update the existing form kwargs dict with the request's user.
            kwargs.update({"request": self.request})
        return kwargs


class GroupRequiredMixin(object):
    """
    Check is the function require any group permission.
    """
    group_required = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            user_groups = []

            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)

            if len(set(user_groups).intersection(self.group_required)) <= 0:
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class BulkEditMixin(object):
    """
    Mixin for views that have a bulk editing facility.  This is normally in the
    form of tabular data where each row has a checkbox.  The UI allows a number
    of rows to be selected and then some 'action' to be performed on them.
    """
    action_param = 'action'

    # Permitted methods that can be used to act on the selected objects
    actions = None
    checkbox_object_name = 'items'

    def get_checkbox_object_name(self):
        if self.checkbox_object_name:
            return self.checkbox_object_name
        return smart_str(self.model._meta.verbose_name_plural.lower())

    def get_error_url(self, request):
        return safe_referrer(request, '.')

    def get_success_url(self, request):
        return safe_referrer(request, '.')

    def get_actions(self):
        return self.actions

    def post(self, request, *args, **kwargs):
        # Dynamic dispatch pattern - we forward POST requests onto a method
        # designated by the 'action' parameter.  The action has to be in a
        # whitelist to avoid security issues.
        action = request.POST.get(self.action_param, '').lower()
        if not self.get_actions() or action not in self.get_actions():
            messages.error(self.request, _("Invalid action."))
            return redirect(self.get_error_url(request))

        ids = request.POST.getlist('selected_%s' % self.get_checkbox_object_name())
        ids = list(map(int, ids))
        if not ids:
            messages.error(
                self.request, _("You need to select some %s.") % self.get_checkbox_object_name()
            )
            return redirect(self.get_error_url(request))

        objects = self.get_objects(ids)
        return getattr(self, action)(request, objects)

    def get_objects(self, ids):
        object_dict = self.get_object_dict(ids)
        # Rearrange back into the original order
        return [object_dict[id] for id in ids]

    def get_object_dict(self, ids):
        return self.get_queryset().in_bulk(ids)
