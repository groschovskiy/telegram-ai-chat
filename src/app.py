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
    

@bot.message_handler(commands=['web'])
def web_handler(message):
    bot.reply_to(message, "Access the full power of our application on your desktop! Visit https://gemini.google.com for a more convenient experience.")


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.reply_to(message, "Explore the official Gemma models website to learn more about them and discover what questions you have. Open https://ai.google.dev/gemma website for more information.")


@bot.message_handler(commands=['models'])
def model_handler(message):
    bot.reply_to(message, "You can send command /set <model> to change the model. For example, /set llama3-8b-8192 or /set mixtral-8x7b-32768")


@bot.message_handler(commands=['set'])
def setup_handler(message):
    rdb.set_ai_model(message.from_user.id, message.text.split(' ')[1])


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
        telebot.types.BotCommand("models", "List of available models"),
    ],
)

cmd = bot.get_my_commands(scope=None, language_code=None)
bot.infinity_polling()
