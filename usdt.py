import requests
import os
import asyncio
import random
import sys
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

TELEGRAM_BOT_TOKEN = "8211368302:AAFIP2fUIrf2g_LnzEboAQpHr0nC6uUAUws"
TELEGRAM_CHANNEL_ID = "-1003567287262"

title = "Deposit,Payout"
title_percent = "50,50" 
button = "🚀 Start Earn 🚀,🎁 Join Community 🎁"
link = "https://t.me/DogeEarn_app_bot,https://t.me/crypto_dogecoin2"
img = "deposit.jpg,payout.jpg" 

DOGE_API_URL = "https://api.blockchair.com/dogecoin/transactions?limit=10"
MIN_AMOUNT = 10
MAX_AMOUNT = 100000000


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LAST_TX_FILE = os.path.join(BASE_DIR, "last_doge_tx.txt")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_last_transaction():
    if os.path.exists(LAST_TX_FILE):
        try:
            with open(LAST_TX_FILE, "r") as file:
                return file.read().strip()
        except: return None
    return None

def save_last_transaction(tx_hash):
    try:
        with open(LAST_TX_FILE, "w") as file:
            file.write(tx_hash)
    except: pass

async def track_and_send():
    print(f"🚀 Active")
    print(f"❤️ Power By @alon_boy_24 telegram")
    
    title_list = [t.strip() for t in title.split(",")]
    weight_list = [int(p.strip()) for p in title_percent.split(",")]
    btn_list = [b.strip() for b in button.split(",")]
    lnk_list = [l.strip() for l in link.split(",")]
    img_list = [i.strip() for i in img.split(",")]

    keyboard = []
    for btn_text, btn_link in zip(btn_list, lnk_list):
        keyboard.append([InlineKeyboardButton(text=btn_text, url=btn_link)])
    reply_markup = InlineKeyboardMarkup(keyboard)

    while True:
        try:
            response = requests.get(DOGE_API_URL, timeout=15)
            if response.status_code != 200:
                await asyncio.sleep(40)
                continue

            res_data = response.json()
            if 'data' in res_data and len(res_data['data']) > 0:
                last_saved_hash = get_last_transaction()
                transactions = res_data['data']
                current_newest_hash = transactions[0]['hash']
                
                new_txs_to_process = []
                for tx in transactions:
                    if tx['hash'] == last_saved_hash:
                        break
                    new_txs_to_process.append(tx)
                
                to_send = list(reversed(new_txs_to_process))[:3]
                
                for tx in to_send:
                    tx_hash = tx['hash']
                    amount = float(tx['output_total']) / 100000000 

                    if MIN_AMOUNT <= amount <= MAX_AMOUNT:
                        indices = list(range(len(title_list)))
                        chosen_idx = random.choices(indices, weights=weight_list, k=1)[0]
                        selected_type = title_list[chosen_idx]

                        if "Deposit" in selected_type:
                            message_text = (
                                f"📥 <b>NEW DEPOSIT</b>\n\n"
                                f"🅰 <b>Amount:-</b> {amount:,.2f} DOGE\n\n"
                                f"🔗 <b>TXID:-</b> <a href='https://blockchair.com/dogecoin/transaction/{tx_hash}'>View Transaction</a>"
                            )
                        else:
                            message_text = (
                                f"✅ <b>SUCCESSFUL PAYOUT</b>\n\n"
                                f"💳 <b>Method:</b> Dogecoin (DOGE)\n"
                                f"🅰 <b>Amount:</b> {amount:,.2f} DOGE\n"
                                f"♦️ <b>Address:</b> <code>D{tx_hash[:25]}...</code>\n"
                                f"⌚ <b>Status:</b> Completed\n"
                                f"📊 <b>Blockchain TXID:</b>\n"
                                f"<a href='https://blockchair.com/dogecoin/transaction/{tx_hash}'>{tx_hash}</a>"
                            )

                        photo_to_send = None
                        if img.lower() != "none" and chosen_idx < len(img_list):
                            img_path = os.path.join(BASE_DIR, img_list[chosen_idx])
                            if os.path.exists(img_path):
                                photo_to_send = open(img_path, 'rb')

                        try:
                            if photo_to_send:
                                await bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=photo_to_send, caption=message_text, parse_mode="HTML", reply_markup=reply_markup)
                                photo_to_send.close() 
                            else:
                                await bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message_text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=reply_markup)
                            print(f"✅ Transaction Sent: {amount} DOGE")
                        except Exception as e: 
                            print(f"❌ Error sending: {e}")

                save_last_transaction(current_newest_hash)

        except Exception as e: 
            print(f"❌ loop error: {e}")
        await asyncio.sleep(40)

if __name__ == "__main__":
    try:
        asyncio.run(track_and_send())
    except KeyboardInterrupt:
        pass
