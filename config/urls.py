from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
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
products_router = routers.NestedSimpleRouter(router, r'products', lookup='product')
products_router.register(r'reviews', ReviewViewSet, basename='product-reviews')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(products_router.urls)),
    path('api/auth/', include('rest_framework.urls')),  # For browsable API login
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]