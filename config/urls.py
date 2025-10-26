from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

# Health check view
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return JsonResponse({
        'status': 'ok',
        'service': 'ecommerce-api',
        'version': '1.0.0'
    })

from api.views import (
    CategoryViewSet, 
    ProductViewSet, 
    OrderViewSet, 
    ReviewViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Main router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

# Nested router for product reviews
products_router = NestedSimpleRouter(router, r'products', lookup='product')
products_router.register(r'reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    # Health check endpoint (no auth required)
    path('api/health/', health_check, name='health-check'),
    
    # Admin site
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/', include(products_router.urls)),
    
    # Authentication
    path('api/auth/', include('rest_framework.urls')),  # For browsable API login
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]