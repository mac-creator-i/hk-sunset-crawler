import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai # Swap to google-genai if using Gemini

# --- PART 1: SCRAPING & PARSING LOGIC ---
def scrape_and_process():
    # Insert the full scraper function we built earlier here...
    # For now, let's assume 'structured_json' holds the AI extracted spots:
    sample_spots = {
        "sunset_spots": [
            {"spot_name_zh": "西環鐘聲泳棚", "district": "堅尼地城", "how_to_get_there": "堅尼地城站C出口步行15分鐘", "is_new_or_trending": "近期Threads上爆紅的落日海景打卡點"}
        ]
    }
    return sample_spots

# --- PART 2: EMAIL SENDING LOGIC ---
def send_email(data):
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD") # App Password, not normal password
    receiver_email = "camilla.cy.lam@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"🌅 Daily HK New Sunset Spots Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    # Format the data into a readable HTML body
    html_content = "<h2>Here are the new sunset spots found over the last 3 months:</h2>"
    for spot in data.get("sunset_spots", []):
        html_content += f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
            <h3 style="color: #FF5A5F;">{spot['spot_name_zh']} ({spot.get('district', 'HK')})</h3>
            <p><b>Transport:</b> {spot['how_to_get_there']}</p>
            <p><b>Why it's trending:</b> {spot['is_new_or_trending']}</p>
        </div>
        """
    
    msg.attach(MIMEText(html_content, 'html'))
    
    # Connect to Google's SMTP Server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587) # Or 587 depending on system settings
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✉️ Report sent successfully to Camilla!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    results = scrape_and_process()
    send_email(results)
