from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from services.google_calendar import get_unavailable_dates, get_unavailable_times


def unavailable_dates(request):
    dates = get_unavailable_dates()
    return JsonResponse({"unavailable": dates})


def unavailable_times(request):
    date = request.GET.get("date")
    if not date:
        return JsonResponse({"error": "Date parameter is required"}, status=400)

    times = get_unavailable_times(date)
    return JsonResponse({"unavailable": times})

# Create your views here.
def index(request):
    return render(request, 'index.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        preferred_date = request.POST.get("preferred_date")
        preferred_time = request.POST.get("preferred_time")
        message = request.POST.get("message")

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

        send_mail(
            subject="New Photography Enquiry",
            message=email_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        return redirect("index")