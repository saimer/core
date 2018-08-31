from django import template

register = template.Library()


@register.filter
def add_placeholder(field, placeholder):
    """
    Add html placeholder for given field.
    """
    field.field.widget.attrs['placeholder'] = placeholder
    return field


@register.filter
def add_class(field, class_name):
    """
    Add html class for given field.
    """
    if field.field.widget.attrs.get('class'):
        default_class = field.field.widget.attrs.get('class').split(" ")
        addon_class = class_name.split(" ")
        combined_class = default_class + list(set(addon_class) - set(default_class))
        field.field.widget.attrs['class'] = " ".join(combined_class)
    else:
        field.field.widget.attrs['class'] = class_name
    return field
