import os
import requests
from msal import ConfidentialClientApplication

# Read secrets from environment
CLIENT_ID = os.environ["ONEDRIVE_CLIENT_ID"]
CLIENT_SECRET = os.environ["ONEDRIVE_CLIENT_SECRET"]

# For personal Microsoft accounts
AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["https://graph.microsoft.com/.default"]

# Authenticate
app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)
result = app.acquire_token_for_client(SCOPES)

if "access_token" not in result:
    print("Failed to get token:", result.get("error"), result.get("error_description"))
    exit(1)

token = result["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Files in OneDrive (My Files)
files = [
    ("work_hour_data", "tft_with_lead_2025-07-10.csv"),
    ("emp_details", "summary_2025-07-11.csv"),
    ("dept_tft_work_hour", "dept_tft_intern_count_2025-07-10.csv"),
]

# Download
for folder, filename in files:
    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{folder}/{filename}:/content"
    out_dir = f"data/{folder}"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{filename}"

    print(f"Downloading {filename} from OneDrive...")
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(resp.content)
        print(f"Saved to {out_path}")
    else:
        print(f"Failed to download {filename}: {resp.status_code} {resp.text}")
