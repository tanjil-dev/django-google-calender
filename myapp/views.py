from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from services.google_calendar import get_unavailable_dates, get_unavailable_times
import logging

logger = logging.getLogger(__name__)

def unavailable_dates(request):
    dates = get_unavailable_dates()
    return JsonResponse({"unavailable": dates})

def unavailable_times(request):
    date = request.GET.get("date")
    if not date:
        return JsonResponse({"error": "Date parameter is required"}, status=400)

    times = get_unavailable_times(date)
    return JsonResponse({"unavailable": times})

def index(request):
    return render(request, 'index.html')

def contact_api(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        preferred_date = request.POST.get('preferred_date')
        preferred_time = request.POST.get('preferred_time')
        message = request.POST.get('message')

        email_message = f"""
        New Enquiry Received

        Name: {name}
        Email: {email}
        Phone: {phone}
        Address: {address}
        Preferred Date: {preferred_date}
        Preferred Time: {preferred_time}

        Message:
        {message}
        """

        try:
            send_mail(
                subject=f"New Photography Enquiry from {name}",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Success!'}, status=200)

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return JsonResponse({'error': 'There was an error sending your message.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
