from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import EmailMessage
from newapp.models import Employee
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
import os
import json
import logging

logger = logging.getLogger(__name__)

# Ensure MEDIA_ROOT is properly configured in settings.py
MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT', 'media')
MEDIA_URL = getattr(settings, 'MEDIA_URL', '/media/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('newapp:home')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

@login_required
def home(request):
    total_users = Employee.objects.count()
    services_done = Employee.objects.filter(service_status="Done").count()
    services_pending = Employee.objects.filter(service_status="Pending").count()
    two_wheeler_count = Employee.objects.filter(vehicle_type="2W").count()
    four_wheeler_count = Employee.objects.filter(vehicle_type="4W").count()

    context = {
        "total_users": total_users,
        "services_done": services_done,
        "services_pending": services_pending,
        "two_wheeler_count": two_wheeler_count,
        "four_wheeler_count": four_wheeler_count,
    }
    return render(request, 'home.html', context)

# List and Create View with Pagination
@login_required
def user(request):
    service = Employee.objects.all()
    paginator = Paginator(service, 5)  # Show 5 entries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Use page_obj instead of service for pagination
    }
    return render(request, 'user.html', context)

def add_user(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        reg_number = request.POST.get('reg_number')
        due_date = request.POST.get('due_date')
        service_status = request.POST.get('service_status')

        # Save the data to the database
        Employee.objects.create(
            name=name,
            email=email,
            address=address,
            phone=phone,
            vehicle_type=vehicle_type,
            reg_number=reg_number,
            due_date=due_date,
            service_status=service_status,
        )
        return redirect('newapp:user')  # Replace with your desired redirect

    return render(request, 'user.html')  # Optional for GET request handling

@login_required
def edit_user(request):
    service = Employee.objects.all()
    paginator = Paginator(service, 5)  # Show 5 entries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Use page_obj instead of service for pagination
    }
    return render(request, 'user.html', context)

def edit(request, id):
    employee = get_object_or_404(Employee, id=id)

    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.address = request.POST.get('address')
        employee.phone = request.POST.get('phone')
        employee.vehicle_type = request.POST.get('vehicle_type')
        employee.reg_number = request.POST.get('reg_number')
        employee.due_date = request.POST.get('due_date')
        employee.service_status = request.POST.get('service_status')
        employee.save()
        return redirect('newapp:user')

    return render(request, 'user.html', {'employee': employee})

def delete(request, id):
    user = get_object_or_404(Employee, id=id)
    user.delete()
    return redirect('newapp:user')

def table_view(request):
    entries = Employee.objects.all()
    paginator = Paginator(entries, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'user.html', {'page_obj': page_obj})

@login_required
def send_alert(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', 'Service Alert From PZ')
        message = request.POST.get('message', 'Dear User,\n\nThis is an important alert from our service center. Please take the necessary actions.\n\nThank you!\n\nBest Regards,\nPZ Team.')
        recipient_list = Employee.objects.filter(service_status='Pending').values_list('email', flat=True)
        
        if recipient_list:
            try:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=list(recipient_list),
                )
                pdf_filename = 'test.pdf'
                pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
                
                if os.path.exists(pdf_path):
                    with open(pdf_path, 'rb') as pdf_file:
                        email.attach(pdf_filename, pdf_file.read(), 'application/pdf')
                else:
                    return JsonResponse({'success': False, 'error': 'PDF attachment not found'})
                
                email.send(fail_silently=False)
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': f"Error sending email: {str(e)}"})
        else:
            return JsonResponse({'success': False, 'error': 'No users with "Pending" service status found'})
    
    return render(request, 'send_alert.html')

def send_individual_email(request):
    if request.method == "POST":
        to_email = request.POST.get("to_email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        attachment = request.FILES.get("attachment")

        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )
            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)
            email.send()
            messages.success(request, "Email sent successfully.")
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")

        return redirect("newapp:user")

    return redirect("newapp:user")

def service_list(request):
    services = Employee.objects.all()
    paginator = Paginator(services, 5)  # Show 5 entries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "user.html", {"page_obj": page_obj})