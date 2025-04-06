from django.urls import path
from .import views

urlpatterns = [
    path('bookings/',views.viewBookings,name="bookings"), 
    path('api/appointment/', views.appointment_event, name='appointment_event'),
    path("book/", views.book_appointment, name="book_appointment"),
]