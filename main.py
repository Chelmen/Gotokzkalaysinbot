import logging
import sys
import requests

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from bs4 import BeautifulSoup
from lxml import etree


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Салам алейкум! Калайсын?")

async def  help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Звони в 112 или тикай с городу")

async def exchange_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    URL = "https://mironline.ru/support/list/kursy_mir/"

    HEADERS = ({'User-Agent':
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
                        'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    stroke = dom.xpath('/html/body/div[3]/div[2]/div[1]/div/div/div/div/div[2]/table/tbody/tr[5]/td[2]/span/p')[0].text
    point = stroke.replace(',', '.')
    tenge = float(point)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=1 / tenge)


if __name__ == '__main__':
    application = ApplicationBuilder().token('5603629183:AAEWgTvLRmp2DIjxOIg33fCaaB-m8fY9sco').build()


    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help_command)
    mir_handler = CommandHandler('mir',exchange_rate)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(mir_handler)

    application.run_polling()
