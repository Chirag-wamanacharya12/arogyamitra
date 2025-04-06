from django.urls import path
from .views import backup_view, get_table_data

urlpatterns = [
    path('backup-view/', backup_view, name='backup_view'),
    path('backup/get-table-data/', get_table_data, name='get_table_data'),
]
