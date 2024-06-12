import os
import telebot
from groq import Groq
import rdb

bot = telebot.TeleBot(os.environ.get("TG_API_KEY"), parse_mode=None)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


@bot.message_handler(commands=['start'])
def welcome_msg(message):
    bot.reply_to(message, f"""\
👋 Hi {message.from_user.first_name}, I am Google Gemma Bot.
I will help you with writing, planning, learning, and more from Google AI.
I'm also support Meta AI and Mistral AI models.\
""")
    

@bot.message_handler(commands=['help'])
def open_help_page(message):
    bot.reply_to(message, "Explore the official Gemma models website to learn more about them and discover what questions you have. Open https://ai.google.dev/gemma website for more information.")


@bot.message_handler(commands=['model'])
def change_model(message):
    bot.reply_to(message, "While I can only utilize the Google Gemma 7B-it model right now, there might be other ways I can assist you. The Google Gemma 7B-it is fantastic for understanding your questions and requests, but if your task requires a different approach,  let me know what you need and I'll see if there's another way I can be helpful.")


@bot.message_handler(commands=['web'])
def change_model(message):
    bot.reply_to(message, "Access the full power of our application on your desktop! Visit https://gemini.google.com for a more convenient experience.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    llm = rdb.get_ai_model(message.from_user.id)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.text,
            }
        ],
        model=llm,
    )
    bot.reply_to(message, chat_completion.choices[0].message.content, parse_mode='Markdown')


bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("web", "Open Gemini website"),
        telebot.types.BotCommand("help", "Gemma FAQ and help"),
        telebot.types.BotCommand("model", "Change Gemma model"),
    ],
)

cmd = bot.get_my_commands(scope=None, language_code=None)
bot.infinity_polling()
