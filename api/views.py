from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for Render monitoring
    This endpoint is publicly accessible
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'ecommerce-api',
        'version': '1.0.0'
    })
from .models import Category, Product, Order, Review
from .serializers import (
    CategorySerializer, ProductSerializer,
    OrderSerializer, ReviewSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()

    def get_queryset(self):
        if 'product_pk' in self.kwargs:
            return Review.objects.filter(product_id=self.kwargs['product_pk'])
        return Review.objects.all()

    def perform_create(self, serializer):
        if 'product_pk' in self.kwargs:
            serializer.save(
                user=self.request.user,
                product_id=self.kwargs['product_pk']
            )
        else:
            serializer.save(user=self.request.user)
