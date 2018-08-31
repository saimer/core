from django.conf import settings


def project_name(request):
    """
    Add project name to template context via Context Processor
    """
    return {
        'PROJECT_NAME': settings.PROJECT_NAME,
        'VERSION': settings.VERSION
    }
