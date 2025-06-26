# signal_bot.py
import time
import telebot
from config import *
from fetcher import fetch_candles
from strategy import generate_signal
from confidence_core import calculate_confidence

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, "🚀 Ultra Quotex Signal Bot Online!\nSignals every 2–3 mins 📡")

def send_signal(pair, chat_id):
    df = fetch_candles(pair, TIMEFRAME)
    signal, reason = generate_signal(df)
    if signal:
        rsi = df["rsi"].iloc[-1]
        ema = df["ema"].iloc[-1]
        macd = df["macd"].iloc[-1]
        signal_line = df["signal"].iloc[-1]

        confidence = calculate_confidence(rsi, ema, macd, signal_line)

        if confidence >= CONFIDENCE_THRESHOLD:
            msg = f"""
📡 Signal Alert
🪙 Pair: {pair}
🕒 Timeframe: {TIMEFRAME}
📈 Signal: {signal}
🔐 Confidence: {confidence:.2f}%
📊 Reason: {reason}
⏳ Next in: 2–3 mins
"""
            bot.send_message(chat_id, msg)

def run_loop():
    chat_id = None
    while not chat_id:
        updates = bot.get_updates()
        if updates:
            chat_id = updates[-1].message.chat.id
            break
        time.sleep(1)

    while True:
        for pair in PAIR_LIST:
            send_signal(pair, chat_id)
            time.sleep(SIGNAL_INTERVAL)

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_loop).start()
    bot.polling()