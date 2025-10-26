from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import connection
from django.db.utils import OperationalError
from django.http import JsonResponse
import logging
import datetime

logger = logging.getLogger(__name__)

# Health check view
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    logger.info("Health check endpoint called")
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = 'connected'
    except OperationalError as e:
        logger.error(f"Database connection error: {str(e)}")
        db_status = 'disconnected'
    
    return Response({
        'status': 'ok' if db_status == 'connected' else 'error',
        'service': 'ecommerce-api',
        'version': '1.0.0',
        'database': db_status,
        'timestamp': datetime.datetime.utcnow().isoformat()
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
    path('admin/', admin.site.urls),
    path('api/', include([
        # Auth endpoints
        path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        
        # Health check
        path('health/', health_check, name='health-check'),
        
        # Countries app
        path('countries/', include('countries.urls')),
        
        # E-commerce app
        path('', include(router.urls)),
        path('', include(products_router.urls)),  # Include nested routes
    ])),
]