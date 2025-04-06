from django.urls import path,include
from .import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image'),
    path('profile/#addFamilyDoctor', views.add_family_doctor, name='addFamilyDoctor'),
    path('profile/#editFamilyDoctor', views.update_family_doctor, name='editFamilyDoctor'),
    path('editprofile/', views.editProfile, name='edit_profile'),
    path('update-details/', views.update_details, name='update_details'),
    path('update_address/', views.update_address, name='update_address'),
    path('add_address/', views.add_address, name='add_address'),
    path('create_family_member/', views.create_family_member, name='create_family_member'),
    path("update_vitals/", views.update_vitals, name="update_vitals"),
    path('create_vitals/', views.create_medical_info, name='create_vitals'),
]