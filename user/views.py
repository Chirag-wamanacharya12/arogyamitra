from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from .models import CustomUser, ContactMessage
from django.contrib import messages


def show(request):
    return render(request, 'home.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        user_type = request.POST.get("user_type")
        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password, user_type=user_type)
            login(request, user)
            return redirect('home')  # Redirect to home after successful registration
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return redirect('login')

    return render(request, 'register.html')

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after login
        else:
            messages.error(request, "Invalid credentials.")
            return HttpResponse('failed to login')

    return render(request, 'login.html')

def logoutView(request):
    logout(request)  # Logs out the current user
    return redirect('login')

def contact(request):
    return render(request, 'contact.html')

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        if name and email and message_text:
            # Save the message to the database
            ContactMessage.objects.create(name=name, email=email, message=message_text)

            # Send confirmation email to the user
            subject = "Thank You for Contacting Us!"
            message = f'''Dear {name},  

                Thank you for reaching out to Arogya Mitra. We have received your message and appreciate your time:  

                You reported for {message_text}

                Our team is reviewing your request and will get back to you as soon as possible. If you need urgent assistance, please feel free to reach
                out to our support team through any of the following channels:  

                📧 Email: arogyamitra.help@gmail.com  
                📞 Phone: +91 9119496893  
                💬 Live Chat: https://www.arogyamitra.com/support 

                We’re here to help!  

                Best regards,  
                Team Arogya Mitra '''

            send_mail(subject, message, "pertinaxstudios@gmail.com", [email], fail_silently=False)

            # Redirect to a success page or display a success message

            messages = "Your message has been sent successfully! A confirmation email has been sent to you."
            return redirect("contact")  # Change "contact" to your actual URL name

    return render(request, "contact.html")


