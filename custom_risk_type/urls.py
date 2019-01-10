from django.conf.urls import url
from . import views

urlpatterns = [
    url('risk-type/(?P<pk>[\w\-]+)', views.InsuranceViewSet.as_view(), name='insurance'),
    url('risk-type/', views.RiskTypeViewSet.as_view(), name='risk-type')
]
