from django.urls import path
from .import views

urlpatterns = [
    path('reports/',views.report,name='reports'),
    path('upload/', views.upload_document, name='upload_document'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
]