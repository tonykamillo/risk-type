from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .serializers import RiskTypeSerializer, InsuranceSerializer
from .models import RiskType, Insurance


class RiskTypeViewSet(generics.ListCreateAPIView):

    queryset = RiskType.objects.all()
    serializer_class = RiskTypeSerializer


class InsuranceViewSet(generics.ListCreateAPIView):
    queryset = Insurance.objects.all()
    serializer_class = InsuranceSerializer

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            risk_type = get_object_or_404(RiskType, pk=pk)
            return Response(RiskTypeSerializer(risk_type).data)
        return super(InsuranceViewSet, self).get(request, **kwargs)
