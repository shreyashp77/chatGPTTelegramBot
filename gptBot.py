import openai
import telegram
from telegram import ext
from keys import telegramKey, openAiKey

# Replace with your actual Telegram token
bot = telegram.Bot(token=telegramKey)

# Replace with your actual API key
openai.api_key = openAiKey


def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        temperature=0.7,
    )

    message = completions.choices[0].text
    return message

# Handle the /start command


def start(update, context):
    update.message.reply_text(
        "Hello! I am a chatbot powered by GPT called Friday.")
    update.message.reply_text(
        "How can I help you today?")
        

# Handle any other message


def message(update, context):
    prompt = update.message.text
    response = generate_response(prompt)
    update.message.reply_text(response)


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
