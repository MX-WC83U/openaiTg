import os
import telegram
import telegram.ext
from dotenv import load_dotenv
import openai

load_dotenv()  # Load the environment variables from the .env file
openai.api_key = os.environ.get('OPENAI_API_KEY')
telegram_api_token = os.environ.get('TELEGRAM_BOT_TOKEN')

# Define the function to generate response using the OpenAI API
def generate_response(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print(response)
    return response.choices[0].message.content.strip()

# Define the function to handle messages
def handle_message(update, context):
    message = update.edited_message if update.edited_message else update.message
    input_text = message.text
    user_info = message.from_user
    response_text = generate_response(input_text)
    
    if update.edited_message:
        message.chat.send_message(response_text, reply_to_message_id=update.edited_message.message_id)
    else:
        message.reply_text(response_text)
    
    # Log the input, response, and user information to a file
    with open('input_response.txt', 'a') as file:
        file.write(f'User: {user_info.username}, chat ID: {user_info.id}\n')
        file.write(f'Input: {input_text}\n')
        file.write(f'Response: {response_text}\n\n')

# Set up the Telegram API connection using the bot token
bot = telegram.Bot(token=telegram_api_token)
updater = telegram.ext.Updater(bot.token, use_context=True)

# Set up the message handler to listen for all messages and respond to them
message_handler = telegram.ext.MessageHandler(filters=telegram.ext.Filters.all, callback=handle_message)
dispatcher = updater.dispatcher
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
