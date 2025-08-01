import os
import requests
from msal import ConfidentialClientApplication

CLIENT_ID = os.environ["ONEDRIVE_CLIENT_ID"]
CLIENT_SECRET = os.environ["ONEDRIVE_CLIENT_SECRET"]

AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["https://graph.microsoft.com/.default"]

app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)
result = app.acquire_token_for_client(SCOPES)

if "access_token" not in result:
    print("Failed to get token:", result.get("error"), result.get("error_description"))
    exit(1)

token = result["access_token"]
headers = {"Authorization": f"Bearer {token}"}

combined_file = "data/combined/combined.csv"

# Upload to OneDrive personal "My Files/combined_data/"
url = "https://graph.microsoft.com/v1.0/me/drive/root:/combined_data/combined.csv:/content"

print("Uploading combined.csv to OneDrive...")
with open(combined_file, "rb") as f:
    resp = requests.put(url, headers=headers, data=f)
    if resp.status_code in [200, 201]:
        print("Upload successful!")
    else:
        print(f"Upload failed: {resp.status_code} {resp.text}")
