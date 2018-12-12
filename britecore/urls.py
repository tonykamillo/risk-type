"""britecore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.conf import settings
# from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic.base import TemplateView

prefix = settings.ENDPOINT_PREFIX


class IndexPage(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPage, self).get_context_data(**kwargs)
        context['prefix'] = prefix
        return context


urlpatterns = [
    # url('%sadmin/' % prefix, admin.site.urls),
    url('api/', include('custom_risk_type.urls')),
    url('', IndexPage.as_view(), name='home')
]
