from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView

from .mixins import RequestFormKwargsMixin


class CoreCreateView(RequestFormKwargsMixin, SuccessMessageMixin, CreateView):
    pass


class CoreUpdateView(RequestFormKwargsMixin, SuccessMessageMixin, UpdateView):
    pass
