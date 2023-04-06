import psutil
import shutil
import time
import telegram

# Telegram bot settings
TELEGRAM_BOT_TOKEN = "<your_bot_token>"
TELEGRAM_CHAT_ID = "<your_chat_id>"

# Disk usage threshold (%)
DISK_USAGE_THRESHOLD = 80

# Memory usage threshold (%)
MEMORY_USAGE_THRESHOLD = 80

# Initialize Telegram bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_notification(subject, message):
    try:
        # 发送硬盘使用量超过阈值的通知
        if "硬盘" in subject:
            message = f"当前硬盘使用量为 {message.strip()}，已经超过阈值，请及时处理！"
        # 发送内存使用量超过阈值的通知
        elif "内存" in subject:
            message = f"当前内存使用量为 {message.strip()}，已经超过阈值，请及时处理！"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{subject}\n{message}")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def check_disk_usage():
    total, used, free = shutil.disk_usage("/")
    used_percent = used / total * 100
    if used_percent > DISK_USAGE_THRESHOLD:
        send_notification("硬盘使用量超过阈值", f"{used_percent:.2f}%")

def check_memory_usage():
    total, available, percent, used, free = psutil.virtual_memory()
    if percent > MEMORY_USAGE_THRESHOLD:
        send_notification("内存使用量超过阈值", f"{percent:.2f}%")

if __name__ == "__main__":
    while True:
        check_disk_usage()
        check_memory_usage()
        time.sleep(60)
