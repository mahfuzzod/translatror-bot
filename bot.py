from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from deep_translator import GoogleTranslator

bot = TeleBot("7895770045:AAETpalW_uB2ZPrVORU1ledNOUkC_DzhxP4") 
user_langs = {}
user_active = {}

languages = {
    "Тоҷикӣ 🇹🇯": "tg",
    "Англисӣ 🇬🇧": "en",
    "Русӣ 🇷🇺": "ru",
    "Арабӣ 🇸🇦": "ar",
    "Фаронсавӣ 🇫🇷": "fr",
    "Хитойӣ 🇨🇳": "zh-CN",
    "Бразилиявӣ 🇧🇷": "pt",
    "Итолиёвӣ 🇮🇹": "it"
}

# Функсия барои эҷоди менюи асосӣ
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("🌐 Интихоби забон"))
    markup.add(KeyboardButton("📋 Меню"), KeyboardButton("⛔ Стоп"))
    return markup

# Функсия барои эҷоди менюи забон
def language_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for lang in languages:
        markup.add(KeyboardButton(lang))
    markup.add(KeyboardButton("🔙 Бозгашт"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_active[message.chat.id] = True
    bot.send_message(
        message.chat.id,
        "👋 Салом! Ман боти тарҷумон ҳастам. Лутфан забонеро интихоб кунед, ки мехоҳед тарҷума шавад.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda msg: msg.text == "🌐 Интихоби забон")
def show_languages(message):
    bot.send_message(
        message.chat.id,
        "📌 Лутфан забонеро интихоб кунед:",
        reply_markup=language_menu()
    )

@bot.message_handler(func=lambda msg: msg.text == "🔙 Бозгашт")
def back_to_menu(message):
    bot.send_message(
        message.chat.id,
        "🔙 Ба менюи асосӣ баргаштед.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda msg: msg.text == "📋 Меню")
def show_menu(message):
    bot.send_message(
        message.chat.id,
        "📋 Ин менюи асосист:\n- 🌐 Интихоби забон\n- ⛔ Стоп барои қатъ кардани бот",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda msg: msg.text == "⛔ Стоп")
def stop_bot(message):
    user_active[message.chat.id] = False
    bot.send_message(
        message.chat.id,
        "⛔ Бот муваққатан қатъ шуд. Барои идома фармони /start ро истифода баред.",
        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/start"))
    )

@bot.message_handler(func=lambda msg: msg.text in languages)
def set_language(message):
    if not user_active.get(message.chat.id, False):
        return
    user_langs[message.chat.id] = languages[message.text]
    bot.send_message(
        message.chat.id,
        f"✅ Шумо забони {message.text} - ро интихоб кардед. Акнун матнро фиристед.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda msg: True)
def translate_text(message):
    chat_id = message.chat.id
    if not user_active.get(chat_id, False):
        return
    if chat_id not in user_langs:
        bot.send_message(chat_id, "❗ Лутфан аввал забонро интихоб кунед.")
        return
    to_lang = user_langs[chat_id]
    try:
        translated = GoogleTranslator(source='auto', target=to_lang).translate(message.text)
        bot.send_message(chat_id, f"🔁 Тарҷума:\n{translated}")
    except Exception as e:
        print(f"[ERROR] Translation failed: {e}")
        bot.send_message(chat_id, "❌ Хатое рух дод дар вақти тарҷума.")

if __name__ == "__main__":
    print("[INFO] Bot is running...")
    bot.polling(none_stop=True)
