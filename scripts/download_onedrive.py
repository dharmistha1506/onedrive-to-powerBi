import os
import json
import requests
from msal import PublicClientApplication

CLIENT_ID = os.environ["ONEDRIVE_CLIENT_ID"]
AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["Files.ReadWrite.All", "offline_access"]

TOKEN_CACHE = "token.json"

def get_token():
    app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

    # If token cache exists, use it
    if os.path.exists(TOKEN_CACHE):
        with open(TOKEN_CACHE, "r") as f:
            cache = json.load(f)
        result = app.acquire_token_silent(SCOPES, account=None)
        if result:
            return result["access_token"]

    # Interactive login
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to create device flow")
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        # Save token cache
        with open(TOKEN_CACHE, "w") as f:
            json.dump(result, f)
        return result["access_token"]
    else:
        raise Exception("Failed to get token: %s" % result)

token = get_token()
headers = {"Authorization": f"Bearer {token}"}

files = [
    ("work_hour_data", "tft_with_lead_2025-07-10.csv"),
    ("emp_details", "summary_2025-07-11.csv"),
    ("dept_tft_work_hour", "dept_tft_intern_count_2025-07-10.csv"),
]

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
