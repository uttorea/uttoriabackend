from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('fullName')
            phone_number = data.get('phoneNumber')
            email = data.get('email')
            reason = data.get('reason')
            message = data.get('message')

            # Basic validation
            if not full_name or not phone_number or not email or not reason or not message:
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Create email content
            subject = f"New Contact Form Submission: {reason}"
            email_message = f"""
            Name: {full_name}
            Phone: {phone_number}
            Email: {email}
            Message: {message}
            """

            # Send the email
            send_mail(
                subject,
                email_message,
                email,  # From email (user's email)
                ['nikhilrai662@gmail.com'],  # To email
                fail_silently=False,
            )

            return JsonResponse({"message": "Form submitted successfully!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method."}, status=400)

from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def send_brochure_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            system = data.get('system')
            full_name = data.get('fullName')
            email = data.get('email')
            
            if not system or not full_name or not email:
                return JsonResponse({'error': 'Missing fields in request data'}, status=400)
            
            # Email content
            subject = 'Brochure Request'
            message = (
                f"This user requested the download brochure of {system}\n"
                f"Name: {full_name}\n"
                f"Email: {email}\n\n"
                f"This user requested the brochure for the {system}."
            )
            from_email = 'your_email@example.com'
            fixed_recipient_email = 'nikhilrai662@gmail.com'
            
            # Send the email to the fixed recipient
            send_mail(subject, message, from_email, [fixed_recipient_email])
            
            return JsonResponse({'message': 'Email sent successfully'})
        except Exception as e:
            logger.error(f'Error processing request: {e}')
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
