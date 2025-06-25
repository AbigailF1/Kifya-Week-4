# scripts/telegram_scraper.py

import os
import json
import pandas as pd
from pyrogram import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


# Telegram API credentials
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise EnvironmentError("❌ Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in your .env file.")

API_ID = int(API_ID)  # convert after checking



# List of e-commerce channels (at least 5)
CHANNELS = [
    "ZemenExpress",
    "nevacomputer",
    "meneshayeofficial",
    "ethio_brand_collection",
    "Leyueqa"
]


def scrape_telegram_channels():
    app = Client("ethiomart_scraper", api_id=API_ID, api_hash=API_HASH)

    all_messages = []

    with app:
        for channel in CHANNELS:
            print(f"\n📥 Scraping from: {channel}")
            try:
                chat_info = app.get_chat(channel)
                channel_title = chat_info.title
                for message in app.get_chat_history(channel, limit=1000):
                    msg_text = message.text or message.caption or ""
                    if not msg_text.strip():
                        continue  # skip empty messages

                    msg_data = {
                        "channel_username": channel,
                        "channel_title": channel_title,
                        "message_id": message.id,
                        "timestamp": message.date.isoformat(),
                        "text": msg_text.strip(),
                        "views": message.views or 0,
                        "media_type": str(message.media) if message.media else None,
                        "has_photo": bool(message.photo),
                        "has_document": bool(message.document)
                    }
                    all_messages.append(msg_data)

            except Exception as e:
                print(f"❌ Error scraping {channel}: {e}")

    if not all_messages:
        print("⚠️ No messages scraped.")
        return

    # Create output folder
    output_folder = "data/raw"
    os.makedirs(output_folder, exist_ok=True)

    # Timestamped file names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(output_folder, f"telegram_messages_{timestamp}.json")
    csv_path = os.path.join(output_folder, f"telegram_messages_{timestamp}.csv")

    # Save as JSON
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(all_messages, f_json, ensure_ascii=False, indent=2)

    # Save as CSV
    df = pd.DataFrame(all_messages)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"\n✅ Scraped {len(all_messages)} messages.")
    print(f"📁 JSON saved to: {json_path}")
    print(f"📁 CSV saved to : {csv_path}")

    return all_messages


if __name__ == "__main__":
    scrape_telegram_channels()