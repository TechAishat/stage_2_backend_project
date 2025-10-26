from django.urls import path
from . import views

urlpatterns = [
    # Country endpoints
    path('', views.CountryListView.as_view(), name='country-list'),
    path('refresh/', views.CountryRefreshView.as_view(), name='country-refresh'),
    path('<str:name>/', views.CountryDetailView.as_view(), name='country-detail'),
    path('image/', views.CountryImageView.as_view(), name='country-image'),
    
    # Status endpoint
    path('status/', views.status_view, name='status'),
]
