from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .api_views import (
    TravelAgentViewSet,
    WebsiteViewSet,
    TravelPackageViewSet,
    ScrapedPackageViewSet,
    PackageMediaViewSet
)
from django.contrib.auth import views as auth_views


# DRF router for API endpoints
router = DefaultRouter()
router.register(r'api/agents', TravelAgentViewSet, basename='agent')
router.register(r'api/websites', WebsiteViewSet, basename='website')
router.register(r'api/packages', TravelPackageViewSet, basename='package')
router.register(r'api/scraped-packages', ScrapedPackageViewSet, basename='scraped-package')
router.register(r'api/media', PackageMediaViewSet, basename='media')

urlpatterns = [
    # Template-based views
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/packages/', views.packages, name='packages'),
    path('dashboard/packages/add/', views.add_package, name='add_package'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/profile/website/delete/<int:website_id>/', views.delete_website, name='delete_website'),
    path('dashboard/search/', views.search_packages, name='search_packages'),
    path('dashboard/search/download/', views.download_results, name='download_results'),
    path('package/<int:pk>/', views.package_detail, name='package_detail'),
    path('dashboard/packages/delete/<int:pk>/', views.delete_package, name='delete_package'),
    path('dashboard/packages/edit/<int:pk>/', views.edit_package, name='edit_package'),


    # API routes
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
