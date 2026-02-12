from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SERVICE_ACCOUNT_FILE = "/home/tanjilahmed/django-google-calender/credentials/test-project-2-432814-427b6b23f9f6.json"
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
            if "date" in event["start"]:  # All-day event
                booked_dates.add(event["start"]["date"])

        # Return the list of unavailable dates
        return list(booked_dates)

    except Exception as e:
        # Catch any errors and print the error message
        print(f"An error occurred: {e}")
        return []


def get_unavailable_times(date):
    try:
        # Authenticate using service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        # Build the Google Calendar service
        service = build("calendar", "v3", credentials=credentials)

        # Set the time range for the selected date
        time_min = datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z"
        time_max = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)).isoformat() + "Z"

        # Log the time range to ensure it's correct
        print(f"TimeMin: {time_min}, TimeMax: {time_max}")

        # Fetch events from the Google Calendar
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        # Get the events
        events = events_result.get("items", [])
        print(f"Events: {events}")

        # If no events are found, return an empty list
        if not events:
            print("No events found on the selected date.")
            return []

        booked_times = []

        # Process each event to get the unavailable times
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            if start:
                booked_times.append(start[11:16])  # HH:MM format

        # Return the list of unavailable times
        return booked_times

    except Exception as e:
        # Catch any errors and print the error message
        print(f"An error occurred: {e}")
        return []


# Example usage (for testing)
if __name__ == "__main__":
    unavailable_dates = get_unavailable_dates()
    print("Unavailable dates:", unavailable_dates)
    unavailable_times = get_unavailable_times("2024-08-01")
    print("Unavailable times on 2024-08-01:", unavailable_times)
