from telegram.ext import Updater, CommandHandler
import gspread
import datetime

gc = gspread.service_account(filename="sheets_service.json")
sheet = gc.open("Weekly_Learning_Plan").sheet1

def start(update, context):
    update.message.reply_text("👋 Hi! I'm your Automation Learning Bot. Use /add <task> to add a new task or /list to view tasks.")

def add(update, context):
    task = " ".join(context.args)
    sheet.append_row([f"Manual Task", task, datetime.datetime.now().isoformat()])
    update.message.reply_text(f"✅ Task added: {task}")

def list_tasks(update, context):
    rows = sheet.get_all_values()
    text = "\n".join([f"{r[0]}: {r[1][:80]}..." for r in rows[-10:]])  # Show last 10
    update.message.reply_text("📋 Recent Tasks:\n" + text)

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_tasks))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
