import requests
from bs4 import BeautifulSoup
import smtplib
import google.generativeai as genai

# CONFIG
URL = "https://example.com/page"
EMAIL = "your@gmail.com"
PASSWORD = "your_app_password"

# Step 1: scrape page
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

content = soup.get_text()[:5000]

# Step 2: analyze with Gemini
genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-pro")

analysis = model.generate_content(
    f"Summarize important changes or insights from this page:\n{content}"
)

result = analysis.text

# Step 3: send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, PASSWORD)
    smtp.sendmail(
        EMAIL,
        EMAIL,
        f"Subject: AI Website Analysis\n\n{result}"
    )
