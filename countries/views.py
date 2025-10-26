from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Country
from .serializers import CountrySerializer, CountryCreateSerializer, CountryUpdateSerializer
import logging

logger = logging.getLogger(__name__)

class CountryListView(APIView):
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'population', 'gdp', 'created_at']
    ordering = ['name']

    def get(self, request):
        try:
            queryset = Country.objects.all()
            
            # Apply search
            search_query = request.query_params.get('search', None)
            if search_query:
                queryset = queryset.filter(name__icontains=search_query)
            
            # Apply ordering
            ordering = request.query_params.get('ordering', self.ordering[0])
            if ordering.lstrip('-') in self.ordering_fields:
                queryset = queryset.order_by(ordering)
            
            serializer = CountrySerializer(queryset, many=True)
            return Response({
                'status': 'success',
                'data': serializer.data,
                'count': len(serializer.data)
            })
        except Exception as e:
            logger.error(f"Error in CountryListView: {str(e)}")
            return Response(
                {'status': 'error', 'message': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = CountryCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating country: {str(e)}")
            return Response(
                {'status': 'error', 'message': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CountryDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, name):
        return get_object_or_404(Country, name__iexact=name)

    def get(self, request, name):
        try:
            country = self.get_object(name)
            serializer = CountrySerializer(country)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Country.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Country not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error in CountryDetailView: {str(e)}")
            return Response(
                {'status': 'error', 'message': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, name):
        try:
            country = self.get_object(name)
            serializer = CountryUpdateSerializer(country, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 'success',
                    'data': serializer.data
                })
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Country.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Country not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating country: {str(e)}")
            return Response(
                {'status': 'error', 'message': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, name):
        try:
            country = self.get_object(name)
            country.delete()
            return Response({
                'status': 'success',
                'message': 'Country deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Country.DoesNotExist:
            return Response(
                {'status': 'error', 'message': 'Country not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting country: {str(e)}")
            return Response(
                {'status': 'error', 'message': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CountryRefreshView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Implement your refresh logic here
        # This is a placeholder - adjust according to your requirements
        return Response({
            'status': 'success',
            'message': 'Countries refreshed successfully'
        })

class CountryImageView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        # Return a default image or list of images
        # This is a placeholder - adjust according to your requirements
        return Response({
            'status': 'success',
            'message': 'Image endpoint',
            'data': []
        })

    def post(self, request):
        # Handle image upload
        # This is a placeholder - adjust according to your requirements
        return Response({
            'status': 'success',
            'message': 'Image uploaded successfully',
            'url': '/path/to/uploaded/image.jpg'
        })

def status_view(request):
    return JsonResponse({
        'status': 'ok',
        'service': 'countries-api',
        'version': '1.0.0',
        'database': 'connected' if Country.objects.exists() else 'disconnected'
    })
