import requests
from bs4 import BeautifulSoup
import smtplib
import google.generativeai as genai
import os

EMAIL = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
API_KEY = os.getenv("GEMINI_API_KEY")

# CONFIG
URL = "https://www.terminalx.com/men/pants/jeans?product_list_order=price_asc"

# Step 1: scrape page
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

content = soup.get_text()[:5000]

# Step 2: analyze with Gemini
genai.configure(api_key=API_KEY)

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
        f"Subject: AI TerminalX Results\n\n{result}"
    )
