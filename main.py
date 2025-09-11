import os
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow
import pathlib

load_dotenv()
app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, "client_secret.json")

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]

@app.get("/auth/login")
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )
    auth_url, state = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def callback(request: Request):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=os.getenv("GOOGLE_REDIRECT_URI")
    )
    flow.fetch_token(authorization_response=str(request.url))
    credential = flow.credentials
    return {
        "access_token": credential.token,
        "refresh_token": credential.refresh_token,
        "expiry": credential.expiry.isoformat()
    }

@app.get("/")
def read_root():
    return {"message": "Hello, Fast API running"}
