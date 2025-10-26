from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.db import connection, DatabaseError
import time
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for Render monitoring
    This endpoint is publicly accessible and checks:
    1. Basic application status
    2. Database connectivity
    """
    response_data = {
        'status': 'ok',
        'service': 'ecommerce-api',
        'version': '1.0.0',
        'timestamp': time.time(),
        'checks': {
            'database': 'ok',
        }
    }
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError as e:
        logger.error(f"Database connection failed: {str(e)}")
        response_data['status'] = 'error'
        response_data['checks']['database'] = 'error'
        response_data['error'] = f"Database error: {str(e)}"
        return JsonResponse(response_data, status=503)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        response_data['status'] = 'error'
        response_data['error'] = str(e)
        return JsonResponse(response_data, status=500)
    
    return JsonResponse(response_data)
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
