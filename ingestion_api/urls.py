# ingestion_api/urls.py
from django.urls import path
from .views import IngestDataView

urlpatterns = [
    path('ingest/', IngestDataView.as_view(), name='ingest-data'),
]