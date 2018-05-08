from django.db import models
from django.contrib.auth.models import UserManager as AbstractUserManager


class UserQuerySet(models.QuerySet):
    """
    User QuerySet
    """

    def filter_by_groups(self, group_list, **kwargs):
        """
        Get user object by given group list.
        """
        return self.filter(
            groups__name__in=group_list, **kwargs
        )


class UserManager(AbstractUserManager.from_queryset(UserQuerySet)):
    pass
