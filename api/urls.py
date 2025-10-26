from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_pk>/reviews/', 
         views.ReviewViewSet.as_view({
             'get': 'list',
             'post': 'create'
         }), name='product-reviews'),
    path('products/<int:product_pk>/reviews/<int:pk>/',
         views.ReviewViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy'
         }), name='review-detail'),
]
