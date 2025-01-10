from telethon import TelegramClient, events
import re
import os
from dotenv import load_dotenv
from x_client import XClient
import pandas as pd


load_dotenv()

# Your API credentials
API_ID = '21451416'
API_HASH = 'c4eecd06ec1f1dfbae429a397b182bd3'
CHANNEL_USERNAME = '@DSTrendingSolana'  # e.g., 'examplechannel'

# Create a client instance
client = TelegramClient('session_name', API_ID, API_HASH)
API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
BEARER_TOKEN = os.environ["BEARER_TOKEN"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
TELE_TOKEN = os.environ['TELE_TOKEN']
TELE_GROUP_ID = os.environ['TELE_GROUP_ID']


x_client = XClient(
    bearer_token= BEARER_TOKEN,
    consumer_key= API_KEY,
    consumer_secret= API_SECRET_KEY,
    access_token= ACCESS_TOKEN,
    access_token_secret= ACCESS_TOKEN_SECRET
)

def extract_x_com_url(message):
    # Regular expression to match x.com URLs
    pattern = r"https://x\.com/([a-zA-Z0-9_]+)"
    match = re.search(pattern, message)

    if match:
        dynamic_name = match.group(1)
        print(f"Extracted Twitter URL: {match.group(0)}")
        print(f"Dynamic Name: {dynamic_name}")
        # Handle the dynamic name here (e.g., logging, processing, etc.)
        return match.group(0), dynamic_name
    else:
        print("No Twitter (x.com) URL found.")
        return None, None
    
def extract_data(text,url, username):
    data = {}
    
    # Basic metrics
    price_match = re.search(r'Price: 🏷️ \$(.+)', text)
    fdv_match = re.search(r'FDV: 🏛️ \$(.+)', text)
    liquidity_match = re.search(r'Liquidity: 💧 \$(.+)', text)
    age_match = re.search(r'Age: 🌿 (.+)', text)
    
    # Volume metrics
    volume_24h = re.search(r'24H: \$(.+)K', text)
    volume_6h = re.search(r'6H: \$(.+)K', text)
    volume_1h = re.search(r'1H: \$(.+)K', text)
    volume_5m = re.search(r'5M: \$(.+)K', text)
    
    # Price changes
    price_24h = re.search(r'24H: [🔴🟢] (.+)%', text)
    price_6h = re.search(r'6H: [🔴🟢] (.+)%', text)
    price_1h = re.search(r'1H: [🔴🟢] (.+)%', text)
    price_5m = re.search(r'5M: [🔴🟢] (.+)%', text)
    
    # Transactions
    txns_total = re.search(r'Total: (\d+)', text)
    txns_buys = re.search(r'Buys: (\d+)', text)
    txns_sells = re.search(r'Sells: (\d+)', text)
    
    # Extract contract address
    ca_match = re.search(r'📄 CA: `(.+)`', text)
    
    data = {
        'Username': username,
        "X_url": url,
        'Price': price_match.group(1) if price_match else '',
        'FDV': fdv_match.group(1) if fdv_match else '',
        'Liquidity': liquidity_match.group(1) if liquidity_match else '',
        'Age': age_match.group(1) if age_match else '',
        'Volume_24H': volume_24h.group(1) if volume_24h else '',
        'Volume_6H': volume_6h.group(1) if volume_6h else '',
        'Volume_1H': volume_1h.group(1) if volume_1h else '',
        'Volume_5M': volume_5m.group(1) if volume_5m else '',
        'Price_Change_24H': price_24h.group(1) if price_24h else '',
        'Price_Change_6H': price_6h.group(1) if price_6h else '',
        'Price_Change_1H': price_1h.group(1) if price_1h else '',
        'Price_Change_5M': price_5m.group(1) if price_5m else '',
        'Total_Transactions': txns_total.group(1) if txns_total else '',
        'Buy_Transactions': txns_buys.group(1) if txns_buys else '',
        'Sell_Transactions': txns_sells.group(1) if txns_sells else '',
        'Contract_Address': ca_match.group(1) if ca_match else ''
    }
    
    return data

def save_to_csv(data, filename='../data/token_data.csv'):
    original_df = None
    if os.path.exists(filename):
        original_df = pd.read_csv(filename)
    df = pd.DataFrame([data])
    if original_df is not None: df = pd.concat([original_df, df], ignore_index= True)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def new_message_listener(event):
    fulltext = event.text
    url, x_username = extract_x_com_url(fulltext)
    data = extract_data(fulltext, url, x_username)
    save_to_csv(data)

async def main():

    print("Listening to messages...")
    await client.run_until_disconnected()

# Start the client and listen for messages
client.start()
client.loop.run_until_complete(main())
