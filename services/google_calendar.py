from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SERVICE_ACCOUNT_FILE = "/home/tanjilahmed/django-google-calender/credentials/test-project-2-432814-427b6b23f9f6.json"
#SERVICE_ACCOUNT_FILE = "credentials/test-project-2-432814-427b6b23f9f6.json"
CALENDAR_ID = "brooksayboy@gmail.com"

print(SERVICE_ACCOUNT_FILE)
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
        slots = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
        
        from collections import defaultdict
        events_by_date = defaultdict(list)

        # Process each event to get the unavailable dates
        for event in events:
            if "date" in event["start"]:  # All-day event
                booked_dates.add(event["start"]["date"])
            elif "dateTime" in event["start"]:
                # Group time-specific events by date
                date_str = event["start"]["dateTime"].split("T")[0]
                events_by_date[date_str].append(event)

        # Check if any dates with time-specific events have ALL slots booked
        for date_str, day_events in events_by_date.items():
            if date_str in booked_dates:
                continue
                
            day_booked_times = set()
            for event in day_events:
                start_str = event["start"].get("dateTime").replace("Z", "+00:00")
                end_str = event["end"].get("dateTime").replace("Z", "+00:00")
                
                try:
                    event_start = datetime.fromisoformat(start_str)
                    event_end = datetime.fromisoformat(end_str)
                except ValueError:
                    continue

                for slot in slots:
                    slot_start_str = f"{date_str}T{slot}:00"
                    try:
                        slot_start = datetime.fromisoformat(slot_start_str).replace(tzinfo=event_start.tzinfo)
                        slot_end = slot_start + timedelta(hours=1)
                        buffer = timedelta(hours=1)
                        if (event_start - buffer) < slot_end and (event_end + buffer) > slot_start:
                            day_booked_times.add(slot)
                    except ValueError:
                        continue
            
            # If all slots are booked, mark the entire date as unavailable
            if len(day_booked_times) >= len(slots):
                booked_dates.add(date_str)

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

        booked_times = set()
        slots = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

        # Process each event to get the unavailable times
        for event in events:
            start_str = event["start"].get("dateTime")
            end_str = event["end"].get("dateTime")

            # All-day events block all slots
            if not start_str and event["start"].get("date"):
                booked_times.update(slots)
                continue

            if start_str and end_str:
                start_str = start_str.replace("Z", "+00:00")
                end_str = end_str.replace("Z", "+00:00")

                try:
                    event_start = datetime.fromisoformat(start_str)
                    event_end = datetime.fromisoformat(end_str)
                except ValueError:
                    continue

                for slot in slots:
                    slot_start_str = f"{date}T{slot}:00"
                    try:
                        slot_start = datetime.fromisoformat(slot_start_str).replace(tzinfo=event_start.tzinfo)
                        slot_end = slot_start + timedelta(hours=1)

                        # Check for strict overlap (no extra 1-hour buffer)
                        if event_start < slot_end and event_end > slot_start:
                            booked_times.add(slot)
                    except ValueError:
                        continue

        # Return the list of unavailable times
        return sorted(list(booked_times))

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
