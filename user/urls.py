from django.urls import path
from .import views

urlpatterns = [
    path('',views.show, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('contact/', views.contact, name='contact'),
    path("message/", views.contact_view, name="message"),
]
