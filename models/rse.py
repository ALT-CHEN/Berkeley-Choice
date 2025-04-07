import fitz  # PyMuPDF
import requests
import os

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def extract_skills_from_resume(pdf_path, threshold=1):
    # EMSI API credentials from environment variables or config
    client_id = os.getenv("EMSI_CLIENT_ID")
    client_secret = os.getenv("EMSI_CLIENT_SECRET")

    auth_url = "https://auth.emsicloud.com/connect/token"
    skills_url = "https://emsiservices.com/skills/versions/latest/extract"

    auth_payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "emsi_open"
    }

    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}

    auth_response = requests.post(auth_url, data=auth_payload, headers=auth_headers)
    if auth_response.status_code != 200:
        print("Error getting access token:", auth_response.status_code, auth_response.text)
        return auth_response.status_code, []

    access_token = auth_response.json().get("access_token")

    payload = {
        "text": extract_text_from_pdf(pdf_path),
        "confidenceThreshold": threshold
    }

    querystring = {"language": "en"}

    skills_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    skills_response = requests.post(skills_url, json=payload, headers=skills_headers, params=querystring)

    if skills_response.status_code == 200:
        skills_data = skills_response.json()
        skill_names = [item["skill"]["name"] for item in skills_data["data"]]
        return 200, skill_names

    return skills_response.status_code, []
