import time
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from selenium import webdriver
from fpdf import FPDF
from bs4 import BeautifulSoup

TOKEN = "8004025144:AAFpRh08w0xZuPKtukuquH_H_l2hP5NZZX4"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Send /getpdf to receive Wingo results as PDF.")

async def getpdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Collecting results...")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.66lottery20.com/#/pages/games/wingo/wingo")
    time.sleep(12)  # Wait for full JavaScript load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.select('.result-record-item')
    driver.quit()

    results = []
    for item in items:
        results.append(item.get_text(strip=True))

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="66Lottery Wingo Results", ln=True, align="C")

    for line in results:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf_file = "wingo_results.pdf"
    pdf.output(pdf_file)

    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(pdf_file, 'rb'))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getpdf", getpdf))
app.run_polling()
