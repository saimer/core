from django.contrib import admin

from ..models import EMPTY_VALUE_DISPLAY


class CoreAdmin(admin.ModelAdmin):
    """
    Use to override all admin to include created and modified.
    """
    empty_value_display = EMPTY_VALUE_DISPLAY
    exclude = ['created_by', 'modified_by', ]

    def get_list_display(self, request):
        """
        Append additional fields to the self.list_display.
        """
        list_display = self.list_display

        if 'admin_created' not in list_display:
            list_display += ('admin_created', )
        if 'admin_modified' not in list_display:
            list_display += ('admin_modified', )

        return list_display

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.current_user = request.user

        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user

        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if not instance.pk and hasattr(instance, 'created_by'):
                instance.created_by = request.user
            elif instance.pk and hasattr(instance, 'modified_by'):
                instance.modified_by = request.user
            instance.save()
        formset.save_m2m()


class CoreTabularInline(admin.TabularInline):
    readonly_fields = ['created_by', 'created', 'modified_by', 'modified', ]
