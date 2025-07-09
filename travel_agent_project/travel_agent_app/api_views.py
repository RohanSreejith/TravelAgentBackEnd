from rest_framework import viewsets, permissions
from .models import TravelAgent, Website, TravelPackage, ScrapedPackage, PackageMedia
from .serializers import (
    TravelAgentSerializer,
    WebsiteSerializer,
    TravelPackageSerializer,
    ScrapedPackageSerializer,
    PackageMediaSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


class TravelAgentViewSet(viewsets.ReadOnlyModelViewSet):  # or ModelViewSet if you want full CRUD
    queryset = User.objects.all()
    serializer_class = TravelAgentSerializer
    permission_classes = [permissions.IsAuthenticated]


class WebsiteViewSet(viewsets.ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class TravelPackageViewSet(viewsets.ModelViewSet):
    serializer_class = TravelPackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TravelPackage.objects.filter(agent=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)


class ScrapedPackageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ScrapedPackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScrapedPackage.objects.filter(agent=self.request.user)


class PackageMediaViewSet(viewsets.ModelViewSet):
    serializer_class = PackageMediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PackageMedia.objects.filter(package__agent=self.request.user)
