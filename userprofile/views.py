import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userprofile.models import FamilyDoctor, PatientVital, Medication, FamilyMember
from user.models import CustomUser, UserAddress
from store.models import Order
from django.contrib import messages


# Create your views here.
def profile(request):
    user = request.user
    Familydoctor = FamilyDoctor.objects.filter(user=user)
    Family = FamilyMember.objects.filter(user=user)

    medications = Medication.objects.filter(user=user)
    from datetime import date
    today = date.today()
    refill_status = ""
    for medication in medications:
        days_until_end = (medication.end_date - today).days
        if medication.end_date == today:
            refill_status = "Completed"
        elif days_until_end <= 5 and medication.refill_reminder:
            refill_status = "Yes"
        else:
            refill_status = "No"
        


    vitals = PatientVital.objects.filter(user=user)
    
    print("Vitals Retrieved:", vitals)
    # Calculate age using the latest recorded vital (if exists)
    age = vitals.latest('recorded_at').age() if vitals.exists() else None  
    bmi = vitals.latest('recorded_at').bmi() if vitals.exists() else None 
    bmi_category = ""

    if bmi is not None:
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            bmi_category = "Normal Weight"
        elif 25 <= bmi < 29.9:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

    myorders = Order.objects.filter(user=user)

    context={
        'user':user,
        'FamilyDoctor' : Familydoctor,
        'medications': medications,
        'refill_status': refill_status,
        'vitals': vitals,
        'age': age,
        'bmi': bmi,
        'Family': Family,
        'bmi_category': bmi_category,
        'myorders': myorders,
    }
    return render(request, 'userprofile/profile.html',context)

def update_profile_image(request):
    user = request.user
    profileImage = CustomUser.objects.get(id=user.id)
    profile, created = CustomUser.objects.get_or_create(id=user.id)

    if request.method == "POST" and request.FILES.get("profile_image"):
        # Save new image
        profile.profile_image = request.FILES["profile_image"]
        profile.save()
        return redirect("profile")  # Redirect to refresh the page

    return render(request, "profile.html", {"profile": profile, 'profileImage':profileImage})

def add_family_doctor(request):
    if request.method == "POST":
        print(request.POST)  # Debugging: Check if data is received
        print(request.FILES) 
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        specialization = request.POST.get("specialization")
        clinic_address = request.POST.get("clinic_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        hospital_affiliation = request.POST.get("hospital_affiliation", "")
        years_of_experience = request.POST.get("years_of_experience")
        profile_image = request.FILES.get("profileImage")

        # Check if required fields are filled
        if not (full_name or phone or email or specialization or clinic_address or city or state or zip_code or years_of_experience):
            return render(request, "userprofile/profile.html", {"error": "All fields are required!"})

        # Save to database
        family_doctor = FamilyDoctor.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            email=email,
            specialization=specialization,
            clinic_address=clinic_address,
            city=city,
            state=state,
            zip_code=zip_code,
            hospital_affiliation=hospital_affiliation,
            years_of_experience=years_of_experience,
            profileImage=profile_image
        )

        family_doctor.save()
        print("Doctor saved successfully!")
        return redirect("/profile/#Dashboard")  # Redirect after successful submission

    return render(request, "userprofile/profile.html")

def update_family_doctor(request):
    user = request.user
    family_doctor_qs = FamilyDoctor.objects.filter(user=user)  # Queryset

    context = {
        "user": user,
        "FamilyDoctor": family_doctor_qs.first(),  # Pass actual object to the template
    }

    if family_doctor_qs.exists() and request.method == "POST":
        print(request.POST)  # Debugging: Check if data is received
        print(request.FILES)

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        specialization = request.POST.get("specialization")
        clinic_address = request.POST.get("clinic_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        hospital_affiliation = request.POST.get("hospital_affiliation", "")
        years_of_experience = request.POST.get("years_of_experience")

        # Check if required fields are filled
        if not (full_name and phone and email and specialization and clinic_address and city and state and zip_code and years_of_experience):
            return render(
                request,
                "userprofile/profile.html",
                {"error": "All fields are required!"},
            )

        # Update the existing FamilyDoctor record
        family_doctor_qs.update(
            full_name=full_name,
            phone=phone,
            email=email,
            specialization=specialization,
            clinic_address=clinic_address,
            city=city,
            state=state,
            zip_code=zip_code,
            hospital_affiliation=hospital_affiliation,
            years_of_experience=years_of_experience,
        )

        print("Doctor updated successfully!")
        return redirect("/profile/#Dashboard")  # Redirect after successful update

    return render(request, "userprofile/profile.html", context)

def editProfile(request):
    user = request.user
    address = UserAddress.objects.filter(user=user)
    patientVital = PatientVital.objects.filter(user=user)
    context = {
        'user':user,
        'userAddress':address,
        'patientVital':patientVital,
    }
    return render(request, 'userprofile/editProfile.html',context)

def update_details(request):
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')  # Match model field name
        user_gender = request.POST.get('user_gender')    # Match model field name
        date_of_birth = request.POST.get('date_of_birth')
        profile_image = request.FILES.get('profile_image')

        try:
            # Handle profile image first
            if profile_image:
                if user.profile_image:
                    try:
                        if os.path.isfile(user.profile_image.path):
                            os.remove(user.profile_image.path)
                    except Exception as e:
                        print(f"Error deleting old image: {e}")

                user.profile_image = profile_image

            # Update user fields
            user.email = email
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.user_gender = user_gender
            user.date_of_birth = date_of_birth
            user.save()

            messages.success(request, "Profile updated successfully!")
            return redirect('edit_profile')
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")
            return redirect('edit_profile')

    return redirect('edit_profile')

def update_address(request):
    user = request.user
    address = UserAddress.objects.filter(user=user)

    if not address.exists():
        messages.error(request, "Address not found!")
        return redirect("profile")

    if request.method == "POST":
        houseNo = request.POST.get("houseNo")
        street_address = request.POST.get("street_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        is_default = request.POST.get("is_default") == "on"

        # If this address is set as default, update other addresses
        if is_default:
            UserAddress.objects.filter(user=user).update(is_default=False)

        address.update(
            houseNo=houseNo,
            street_address=street_address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            is_default=is_default,
        )

        messages.success(request, "Address updated successfully!")
        return redirect("profile")

    context = {"address": address.first()}
    return redirect('edit_profile')

def add_address(request):
    user = request.user

    if request.method == "POST":
        houseNo = request.POST.get("houseNo")
        street_address = request.POST.get("street_address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")
        postal_code = request.POST.get("postal_code")
        is_default = request.POST.get("is_default") == "on"

        UserAddress.objects.create(  # ✅ Fix: use the model manager
            user=user,
            houseNo=houseNo,
            street_address=street_address,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            is_default=is_default,
        )

        messages.success(request, "Address added successfully!")
        return redirect("profile")

    return redirect('edit_profile')  # You can add context here if needed

def create_family_member(request):
    if request.method == "POST":
        name = request.POST.get("name")
        relationship = request.POST.get("relationship")
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        contact_number = request.POST.get("contact_number")

        FamilyMember.objects.create(
            user=request.user,
            name=name,
            relationship=relationship,
            date_of_birth=date_of_birth if date_of_birth else None,
            gender=gender,
            contact_number=contact_number
        )
        return redirect("profile")  # Redirect to profile page after creation

    return redirect("profile")  

@login_required
def update_vitals(request):
    user = request.user
    try:
        vitals = PatientVital.objects.get(user=user)
    except PatientVital.DoesNotExist:
        messages.error(request, "Vital record not found.")
        return redirect('profile')  # or wherever

    if request.method == "POST":
        vitals.blood_pressure_systolic = request.POST.get("blood_pressure_systolic")
        vitals.blood_pressure_diastolic = request.POST.get("blood_pressure_diastolic")
        vitals.heart_rate = request.POST.get("heart_rate")
        vitals.glucose = request.POST.get("glucose")
        vitals.cholesterol = request.POST.get("cholesterol")
        vitals.weight = request.POST.get("weight")
        vitals.height = request.POST.get("height")
        vitals.save()

        messages.success(request, "Vitals updated successfully.")
        return redirect("profile")  # or any page

    return render(request, "userprofile/editProfile.html")

@login_required
def create_medical_info(request):
    if request.method == "POST":
        blood_group = request.POST.get("blood_group")
        systolic = request.POST.get("blood_pressure_systolic")
        diastolic = request.POST.get("blood_pressure_diastolic")
        heart_rate = request.POST.get("heart_rate")
        glucose = request.POST.get("glucose")
        cholesterol = request.POST.get("cholesterol")
        weight = request.POST.get("weight")
        height = request.POST.get("height")

        # Set a valid birth date; modify as needed based on your data model
        birth_date = request.user.birth_date if hasattr(request.user, 'birth_date') else None
        if not birth_date:
            messages.error(request, "Birth date is required.")
            return redirect("create_vitals")

        PatientVital.objects.create(
            user=request.user,
            birth_date=birth_date,
            blood_group=blood_group,
            blood_pressure_systolic=systolic,
            blood_pressure_diastolic=diastolic,
            heart_rate=heart_rate,
            glucose=glucose,
            cholesterol=cholesterol,
            weight=weight,
            height=height,
        )

        messages.success(request, "Medical info created successfully.")
        return redirect("profile")  # or your desired page

    return render(request, "userprofile/editProfile.html")
