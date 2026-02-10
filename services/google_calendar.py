from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SERVICE_ACCOUNT_FILE = "credentials/test-project-2-432814-427b6b23f9f6.json"
CALENDAR_ID = "tanzil.ovi578@gmail.com"


def get_unavailable_dates(days=60):
    try:
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        # Build the Google Calendar service
        service = build("calendar", "v3", credentials=credentials)

        # Get current time and future time for the query
        now = datetime.utcnow().isoformat() + "Z"
        future = (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"

        # Log the time range to ensure it's correct
        print(f"TimeMin: {now}, TimeMax: {future}")

        # Fetch events from the Google Calendar
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            timeMax=future,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        # Get the events
        events = events_result.get("items", [])
        print(f"Events: {events}")

        # If no events are found, return an empty list
        if not events:
            print("No events found in the given date range.")
            return []

        booked_dates = set()

        # Process each event to get the unavailable dates
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            if start:
                booked_dates.add(start[:10])  # YYYY-MM-DD format

        # Return the list of unavailable dates
        return list(booked_dates)

    except Exception as e:
        # Catch any errors and print the error message
        print(f"An error occurred: {e}")
        return []


# Call the function and print the unavailable dates
unavailable_dates = get_unavailable_dates()
print("Unavailable dates:", unavailable_dates)
