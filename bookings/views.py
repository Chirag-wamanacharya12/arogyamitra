from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Appointment

def viewBookings(request):
    time_slots = Appointment.TIME_SLOT_CHOICES  # Fetching time slot choices
    patients = CustomUser.objects.all()  # Fetching all patients
    doctors = Doctor.objects.all()  # Fetching all doctors

    context = {
        'time_slots': time_slots,
        'patients': patients,
        'doctors': doctors,
    }

    return render(request,'bookings/bookings.html', context)

from django.utils.timezone import make_aware
from datetime import datetime



# -------------------------------- API View ---------------------------------------#
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer

@api_view(['GET'])
def appointment_event(request):
    """API to return appointments formatted for FullCalendar."""
    appointments = Appointment.objects.all() # Show only user's appointments
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
# ---------------------------------------------------------------------------------#

from user.models import CustomUser, Doctor
from django.utils.timezone import now

def book_appointment(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient")
        doctor_id = request.POST.get("doctor")
        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")
        preferred_time_slot = request.POST.get("preferred_time_slot")
        appointment_type = request.POST.get("appointment_type")
        appointment_agenda = request.POST.get("appointment_agenda")

        patient = CustomUser.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        # Creating appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            preferred_time_slot=preferred_time_slot,
            appointment_type=appointment_type,
            appointment_agenda=appointment_agenda,
            status="pending",
            payment_status="pending",
            created_at=now()
        )

        return redirect("bookings")

    return render(request, "bookings/bookings.html")
