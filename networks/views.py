from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ElectronicsNetwork
from .permissions import IsActiveEmployee
from .serializers import ElectronicsNetworkSerializer

class ElectronicsNetworkViewSet(viewsets.ModelViewSet):
    queryset = ElectronicsNetwork.objects.all()
    serializer_class = ElectronicsNetworkSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']
    search_fields = ['name', 'city']