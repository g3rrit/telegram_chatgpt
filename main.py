#!/usr/bin/env python3
# Requires
# python-telegram-bot==13.12

import sys
from telegram.ext import Updater, MessageHandler, filters
import os
import openai

TOKEN = os.getenv("TELEGRAM_PEARGPT_TOKEN")
USER = int(os.getenv("TELEGRAM_USER"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

MESSAGES = []


def handle_msg(update, context):
    global MESSAGES

    chat_id = update.effective_chat.id

    if chat_id != USER:
        print(f"Invalid chat id {chat_id}")
        sys.exit(-1)

    msg = update.message.text

    if msg.startswith("/new"):
        MESSAGES = []
        context.bot.send_message(chat_id, "Starting new conversation")
        return

    MESSAGES.append({"role": "user", "content": msg})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=MESSAGES,
    )

    res_msg = completion.choices[0].message

    MESSAGES.append(res_msg)

    context.bot.send_message(chat_id, res_msg["content"])


def main():

    print("Starting Server")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    filt = filters.Filters.chat(chat_id=USER)

    dp.add_handler(MessageHandler(filt, handle_msg))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
