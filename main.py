import requests
from bs4 import BeautifulSoup
import smtplib
from google import genai
import os

EMAIL = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
API_KEY = os.getenv("GEMINI_API_KEY")

size = "30W-30L"
avoid_words = "bootcut, skinny, slim, athletic"

# CONFIG
URL = "https://www.terminalx.com/men/pants/jeans?product_list_order=price_asc"

# Step 1: scrape page
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

content = soup.get_text()

# Step 2: analyze with Gemini
client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=f"Summarize in array 'url1,url3,url4,...' all the products with avilable size of {size} and without the words {avoid_words} from this page:\n{content}"
)

result = response.text

# Step 3: send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, PASSWORD)
    smtp.sendmail(
        EMAIL,
        EMAIL,
        f"Subject: AI TerminalX Results\n\n{result}"
    )
