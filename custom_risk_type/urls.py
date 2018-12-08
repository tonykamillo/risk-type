from django.urls import path
from . import views

urlpatterns = [
    path('risk-type/<uuid:pk>', views.InsuranceViewSet.as_view(), name='insurance'),
    path('risk-type/', views.RiskTypeViewSet.as_view(), name='risk-type')
]
