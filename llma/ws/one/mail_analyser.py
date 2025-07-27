import imaplib
import email
import requests
from email.utils import parsedate_to_datetime
from openpyxl import Workbook
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timezone

# Uncomment for verbose IMAP logs
# imaplib.Debug = 4

# ---------------- Load .env ----------------
load_dotenv()
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")
TARGET_SENDER = os.getenv("TARGET_SENDER")

# ---------------- Fetch emails from specific date ----------------
def fetch_email_after_date(sender_email, after_utc):
    print(f"🔄 Connecting to Gmail as {GMAIL_USER}...")
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(GMAIL_USER, GMAIL_PASS)
    imap.select("inbox")

    print(f"🔍 Searching for emails from: {sender_email}")
    status, messages = imap.search(None, f'FROM "{sender_email}"')
    email_ids = messages[0].split()
    print(f"📨 Found {len(email_ids)} emails from {sender_email}")

    for eid in reversed(email_ids):  # Newest first
        print(f"📩 Checking email ID: {eid.decode()}")
        status, msg_data = imap.fetch(eid, "(RFC822)")
        if status != 'OK':
            print("⚠️ Error fetching message:", status)
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        print("📅 Raw Date Header:", msg["Date"])

        try:
            email_date = parsedate_to_datetime(msg["Date"]).astimezone(timezone.utc)
            print("🕒 Parsed Email UTC Date:", email_date.isoformat())
        except Exception as e:
            print("❌ Failed to parse date:", e)
            continue

        print("🕒 Cutoff UTC Date: ", after_utc.isoformat())
        if email_date < after_utc:
            print("⏭️ Skipping old email.")
            continue

        print("✅ New email found. Extracting body...")

        # Get plain text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        imap.logout()
        return body

    imap.logout()
    return None

'''
# ---------------- Feed to LLM ----------------
def parse_with_llm(email_body):
    prompt = f"""
Extract structured tabular data from the following email content and format it in rows and columns. Keep it simple for Excel:
---
{email_body}
---
Output format (in plain text):
Column1 | Column2 | Column3
------ | ------- | -------
value1 | value2  | value3
    """
    print("🤖 Sending to LLM (gemma3)...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        print("✅ LLM response received.")
    else:
        print("❌ LLM request failed:", response.status_code, response.text)

    return response.json().get("response", "")
'''

def parse_with_llm(email_body):
    prompt = f"""
You are an AI assistant. Read the email text below and extract key information like user name, consumed data percentage, and remaining data percentage. Return the output in the following table format:

User | Consumed Data | Remaining Data
-----|---------------|----------------
Mandar | 80% | 20%

Use plain text, no Markdown, and extract only what’s available.

Email:
---
{email_body}
---
"""
    print("🤖 Sending to LLM (gemma3)...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        print("✅ LLM response received.")
    else:
        print("❌ LLM request failed:", response.status_code, response.text)

    return response.json().get("response", "")


# ---------------- Save to Excel ----------------
def save_to_excel(llm_output, filename="output.xlsx"):
    wb = Workbook()
    ws = wb.active

    lines = llm_output.strip().splitlines()
    for line in lines:
        if "|" in line:
            cells = [cell.strip() for cell in line.split("|")]
            ws.append(cells)

    wb.save(filename)
    print("📁 Excel saved as", filename)


if __name__ == "__main__":
    print("📧 Gmail Reader + LLM + Excel (Running until Ctrl+C)")

    if not GMAIL_USER or not GMAIL_PASS or not TARGET_SENDER:
        print("❌ Missing .env values. Please check GMAIL_USER, GMAIL_APP_PASSWORD, TARGET_SENDER.")
        exit(1)

    # 🕒 Set fixed start date for filtering emails
    start_time_utc = datetime(2025, 7, 26, 0, 0, 0, tzinfo=timezone.utc)
    print(f"🕒 Monitoring inbox for emails from {TARGET_SENDER} sent after {start_time_utc.isoformat()}")

    try:
        while True:
            email_body = fetch_email_after_date(TARGET_SENDER, start_time_utc)

            if email_body:
                print("✉️ Email Body:\n", email_body)
                llm_output = parse_with_llm(email_body)
                print("📄 LLM Output:\n", llm_output)
                save_to_excel(llm_output)

                # ✅ update start time to avoid reprocessing
                start_time_utc = datetime.now(timezone.utc)

            print("⏳ Waiting 30 seconds before checking again...\n")
            time.sleep(30)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user (Ctrl+C)")


'''
# ---------------- Main ----------------
if __name__ == "__main__":
    print("📧 Gmail Reader + LLM + Excel (From 26 July 2025)")

    if not GMAIL_USER or not GMAIL_PASS or not TARGET_SENDER:
        print("❌ Missing .env values. Please check GMAIL_USER, GMAIL_APP_PASSWORD, TARGET_SENDER.")
        exit(1)

    # ✅ Fixed date from which to read new emails (26 July 2025, 00:00 UTC)
    start_time_utc = datetime(2025, 7, 26, 0, 0, 0, tzinfo=timezone.utc)
    print(f"🕒 Checking for emails from: {start_time_utc.isoformat()}")

    while True:
        email_body = fetch_email_after_date(TARGET_SENDER, start_time_utc)

        if email_body:
            print("✉️ Email Body:\n", email_body)
            llm_output = parse_with_llm(email_body)
            print("📄 LLM Output:\n", llm_output)
            save_to_excel(llm_output)
            break

        print("⌛ No matching email found. Waiting 30 seconds...\n")
        time.sleep(30)
'''