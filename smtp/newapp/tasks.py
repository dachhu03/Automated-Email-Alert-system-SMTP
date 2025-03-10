from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import os

def get_pdf_attachment():
    """Returns the PDF attachment if it exists."""
    pdf_filename = 'test.pdf'  # Ensure correct path inside media/
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
    
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as pdf_file:
            return pdf_filename, pdf_file.read()
    return None, None

@shared_task
def send_alert_email():
    from newapp.models import Employee  # Import inside function to prevent circular imports

    subject = 'Service Alert'
    message = 'This is an automated alert email from the system.'
    
    recipient_list = Employee.objects.filter(service_status='Pending').values_list('email', flat=True)
    
    if recipient_list:
        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=list(recipient_list),
            )
            
            # Attach PDF if available
            pdf_filename, pdf_content = get_pdf_attachment()
            if pdf_content:
                email.attach(pdf_filename, pdf_content, 'application/pdf')
            
            email.send(fail_silently=False)
            return 'Emails sent successfully'
        except Exception as e:
            return f"Error sending email: {str(e)}"
    
    return 'No users with "Pending" service status found'


# If needed, add additional tasks here as required
