from telebot import TeleBot
from config import BOT_TOKEN
from telebot import custom_filters
from handlers import start, booking, cancellation, admin

bot = TeleBot(BOT_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))

# Handlers registration
start.register_handlers(bot)
booking.register_handlers(bot)
cancellation.register_handlers(bot)
admin.register_handlers(bot)

if __name__ == "__main__":
    bot.infinity_polling()
