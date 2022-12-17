import openai
import telegram
from telegram import ext
from telegram.ext import CommandHandler
from keys import telegramKey, openAiKey

# Replace with your actual Telegram token
bot = telegram.Bot(token=telegramKey)

# Replace with your actual API key
openai.api_key = openAiKey


def generate_response(prompt, previous_prompts, previous_response):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=previous_prompts + "\n" + previous_response + "\n" + prompt,
        max_tokens=2048,
        n=1,
        temperature=0.7,
    )

    try:
        message = completions.choices[0].text
    except Exception as e:
        return ("Error :(\nTry again!")

    if len(message) == 0:
        return "Try again :("
    if message[0] == "?":
        message = message[1:]

    return message


# Handle the /start command


def start(update, context):
    update.message.reply_text(
        "Hello! I am a chatbot powered by GPT called Friday.")
    update.message.reply_text(
        "How can I help you today?")


# Handle any other message


previous_prompt = ""
previous_response = ""


def message(update, context):
    global previous_prompt
    global previous_response
    prompt = update.message.text
    if prompt == "/stop":
        return close(update, context)
    response = generate_response(prompt, previous_prompt, previous_response)
    update.message.reply_text(response)
    previous_prompt = prompt
    previous_response = response


# handle /stop
def close(update, context):
    update.message.reply_text("Ok Bye!")
    updater = telegram.ext.Updater(token=telegramKey, use_context=True)
    updater.stop()


# Set up the Updater and start it
updater = telegram.ext.Updater(
    token=telegramKey, use_context=True)
dispatcher = updater.dispatcher

start_handler = telegram.ext.CommandHandler('start', start)
dispatcher.add_handler(start_handler)

message_handler = telegram.ext.MessageHandler(
    telegram.ext.Filters.text, message)
dispatcher.add_handler(message_handler)

updater.start_polling()
