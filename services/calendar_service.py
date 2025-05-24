from googleapiclient.discovery import build
from google.oauth2 import service_account
from config import GOOGLE_CREDENTIALS_FILE, CALENDAR_ID

SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials = service_account.Credentials.from_service_account_file(
    GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
)

calendar_service = build('calendar', 'v3', credentials=credentials)