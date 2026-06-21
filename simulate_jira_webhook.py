import requests

# The URL pointing directly to our FastAPI webhook receiver
url = "http://127.0.0.1:8000/webhook/jira-story"

# Construct a realistic data payload mimicking an enterprise Jira ticket
mock_jira_payload = {
    "issue_key": "PROD-742",
    "summary": "Biometric Bi-weekly Authentication Bypass Lockout",
    "description": (
        "As a mobile banking user, I want the application to automatically lock my account "
        "if I fail FaceID login 3 consecutive times, so that my financial data remains secure. "
        "Notes: Lockout duration should be exactly 15 minutes. A warning push notification "
        "must be dispatched on the 2nd failed attempt. System administrators should be able "
        "to manually override and unlock the profile via the secure admin dashboard."
    )
}

print("📡 Simulating Jira Webhook Event... Sending payload to local server.")

# Fire the POST request to our running app
try:
    response = requests.post(url, json=mock_jira_payload)
    
    # Print the network confirmation status code and response payload
    print(f"Status Code received from FastAPI: {response.status_code}")
    print(f"Server Response Content: {response.json()}")

except Exception as e:
    print(f"Failed to connect to the local server: {e}")