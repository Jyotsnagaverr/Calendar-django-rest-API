# myapp/views.py

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# Google Calendar credentials
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://your-domain.com/rest/v1/calendar/redirect/'
CLIENT_SECRET_FILE = '../secrets/client_secrets.json'


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials

        # Now, you can use `credentials` to make requests to the Google Calendar API
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        # You can process the events further or return them as a response

        return JsonResponse(events, safe=False)
