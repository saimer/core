"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.utils.translation import gettext_lazy
from django.views.generic.base import RedirectView
from django.conf.urls.static import static

admin.site.site_title = gettext_lazy(
    '{} site admin'.format(settings.PROJECT_NAME)
)
admin.site.site_header = gettext_lazy(
    '{} administration'.format(settings.PROJECT_NAME)
)


urlpatterns = [
    path(
        'favicon.ico',
        RedirectView.as_view(
            url='{0}icons/favicon.ico'.format(settings.STATIC_URL)
        ),
        name='favicon'
    ),

    path('site-admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
