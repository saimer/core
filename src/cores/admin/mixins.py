from sorl.thumbnail.fields import ImageField

from ..widgets import CoreAdminImageWidget


class AdminImageMixin(object):
    """
    This is a mix-in for admin to change ``ImageField`` to use
    CoreAdminImageWidget.
    """

    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, ImageField):
            return db_field.formfield(widget=CoreAdminImageWidget)

        return super().formfield_for_dbfield(db_field, **kwargs)
