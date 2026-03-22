import os
import telebot
from telebot import types
from dotenv import load_dotenv
import threading
import random

# --- ИМПОРТЫ ---
# Импортируем комментарии для входных ботов
import comments_zatoon
import comments_plus
import comments_cash

# Импортируем данные для основного бота (ссылки на UNU и т.д.)
# (Предполагается, что у тебя есть файл data.py с переменной sites)
try:
    from data import sites
except ImportError:
    print("Файл data.py не найден, основной бот не запустится.")
    sites = []
    partner_sites = []

load_dotenv()

# --- ФУНКЦИЯ ДЛЯ ВХОДНЫХ БОТОВ (Ворота) ---
def run_gateway_bot(token, comments_module, bot_name_label):
    if not token:
        print(f"Ошибка: Токен для {bot_name_label} не найден")
        return

    bot = telebot.TeleBot(token)
    MAIN_BOT_LINK = os.getenv('MAIN_BOT_LINK')
    SPAM_TASK_LIMIT = 10
    users_db = {}

    def get_random_text(text_type):
        if text_type == 'ENTRY':
            texts = comments_module.COMMENTS_ENTRY
        else:
            texts = comments_module.COMMENTS_SPAM
        return random.choice(texts) if texts else "Ошибка текста"

    # --- Логика Вороты (Скопирована из твоих прошлых файлов) ---
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        chat_id = message.chat.id
        text = (
            "🎰 <b>Система активного заработка</b>\n\n"
            "Анализирую твой регион... Найдено предложений: 15.\n"
            "⚡️ <b>Доступ к высокооплачиваемым заданиям:</b> <u>Разблокирован</u>.\n\n"
            "⚠️ <b>Внимание:</b> Чтобы отсеять ботов, пройдите быструю проверку.\n\n"
            "👇 Нажмите кнопку ниже, чтобы начать."
        )
        markup = types.InlineKeyboardMarkup()
        btn_start = types.InlineKeyboardButton("🚀 Начать проверку", callback_data="start_verify")
        markup.add(btn_start)
        bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == "start_verify")
    def step_one_start(call):
        chat_id = call.message.chat.id
        comment_text = get_random_text('ENTRY')
        text = (
            "✅ <b>Шаг 1: Подтверждение человека</b>\n\n"
            "Нам нужно убедиться, что вы реальный пользователь.\n\n"
            "1. Найдите комментарий, благодаря которому вы узнали о боте (в TikTok).\n"
            "2. Нажмите 'Ответить' на этот комментарий.\n"
            "3. Скопируйте текст ниже и отправьте ответ.\n\n"
            f"📝 <b>Текст для копирования:</b>\n\n<code>{comment_text}</code>\n\n"
            "📸 Пришлите скриншот вашего ответа сюда."
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text, parse_mode='HTML')
        users_db[chat_id] = {'step': 'wait_entry_photo', 'count': 0}

    @bot.content_types(content_types=['photo'])
    def handle_photos(message):
        chat_id = message.chat.id
        user_data = users_db.get(chat_id)
        if not user_data:
            bot.send_message(chat_id, "Напишите /start для начала работы.")
            return

        if user_data['step'] == 'wait_entry_photo':
            bot.send_message(chat_id, "✅ <b>Отлично! Комментарий найден.</b>", parse_mode='HTML')
            start_spam_stage(chat_id)
        elif user_data['step'] == 'wait_spam_photo':
            user_data['count'] += 1
            current_count = user_data['count']
            if current_count < SPAM_TASK_LIMIT:
                bot.send_message(chat_id, f"✅ <b>Принято {current_count}/{SPAM_TASK_LIMIT}</b>\n\nПродолжаем.", parse_mode='HTML')
                send_spam_task(chat_id)
            else:
                finish_verification(chat_id)

    def start_spam_stage(chat_id):
        users_db[chat_id]['step'] = 'wait_spam_photo'
        text = (
            "🔥 <b>Финальный этап: Расширение доступа</b>\n\n"
            f"Чтобы получить доступ к базе заданий, нужно написать <b>{SPAM_TASK_LIMIT} комментариев</b>.\n\n"
            "Мы будем давать вам текст, вы копируете его и пишете под любым видео в TikTok.\n\n"
            "👇 <b>Текст №1:</b>"
        )
        bot.send_message(chat_id, text, parse_mode='HTML')
        send_spam_task(chat_id)

    def send_spam_task(chat_id):
        comment_text = get_random_text('SPAM')
        text = f"📝 <b>Скопируй текст ниже и напиши под видео:</b>\n\n<code>{comment_text}</code>\n\n📸 Пришли скриншот, когда напишешь."
        bot.send_message(chat_id, text, parse_mode='HTML')

    def finish_verification(chat_id):
        markup = types.InlineKeyboardMarkup()
        btn_final = types.InlineKeyboardButton("🚀 ВОЙТИ В СИСТЕМУ", url=MAIN_BOT_LINK)
        markup.add(btn_final)
        text = (
            "🎉 <b>Модерация пройдена успешно!</b>\n\n"
            "Ты доказал, что ты активный пользователь.\n"
            "Доступ к базе заданий разблокирован.\n\n"
            "👇 Нажми кнопку ниже:"
        )
        bot.send_message(chat_id, text, parse_mode='HTML', reply_markup=markup)
        users_db[chat_id]['step'] = 'done'

    print(f"Входной бот {bot_name_label} запущен...")
    bot.infinity_polling()


# --- ФУНКЦИЯ ДЛЯ ОСНОВНОГО БОТА (KarmanCash) ---
def run_main_bot():
    token = os.getenv('TOKEN_MAIN')
    if not token:
        print("Ошибка: TOKEN_MAIN не найден")
        return

    # ВАЖНО: Инициализируем данные перед запуском
    import data
    data.init_data()

    bot = telebot.TeleBot(token)

    # Проверка
    if not data.sites:
        print("Ошибка: Список сайтов пуст!")
        return

    # Вспомогательные функции (из твоего основного бота)
    def get_site_keyboard(site_id):
        markup = types.InlineKeyboardMarkup()
        site_url = sites[site_id]['link']
        btn_site = types.InlineKeyboardButton(text=f"💸 {sites[site_id]['button_text']}", url=site_url)
        btn_prev = types.InlineKeyboardButton(text="⬅️", callback_data=f"prev_{site_id}")
        btn_next = types.InlineKeyboardButton(text="➡️", callback_data=f"next_{site_id}")
        markup.add(btn_site)
        markup.add(btn_prev, btn_next)
        return markup

    # Хэндлеры основного бота
    @bot.message_handler(commands=['start'])
    def send_welcome_main(message):
        text = (
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            "Это твой навигатор по заработку <b>KarmanCashBot</b>.\n"
            "Я собрал лучшие буксы в одном месте.\n\n"
            "💎 Здесь нет баланса. Я не посредник!\n"
            "Ты регистрируешься на сайтах, и они <b>сразу платят тебе</b>.\n\n"
            "👇 Выбери действие:"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_catalog = types.InlineKeyboardButton("🗂 Каталог сайтов (Заработок)", callback_data="open_catalog")
        btn_partner = types.InlineKeyboardButton("💼 Стать партнером (Пассив)", callback_data="open_partner")
        markup.add(btn_catalog, btn_partner)
        bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query_main(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == "open_catalog":
            site = sites[0]
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"<b>{site['name']}</b>\n\n{site['desc']}", parse_mode='HTML', reply_markup=get_site_keyboard(0))

        elif call.data.startswith("prev_"):
            current_id = int(call.data.split("_")[1])
            prev_id = current_id - 1
            if prev_id < 0: prev_id = len(sites) - 1
            site = sites[prev_id]
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"<b>{site['name']}</b>\n\n{site['desc']}", parse_mode='HTML', reply_markup=get_site_keyboard(prev_id))

        elif call.data.startswith("next_"):
            current_id = int(call.data.split("_")[1])
            next_id = current_id + 1
            if next_id >= len(sites): next_id = 0
            site = sites[next_id]
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"<b>{site['name']}</b>\n\n{site['desc']}", parse_mode='HTML', reply_markup=get_site_keyboard(next_id))

        elif call.data == "open_partner":
            text = (
                "💼 <b>Хочешь пассивный доход?</b>\n\n"
                "Ты можешь зарабатывать не только кликая кнопками, но и приглашая друзей.\n\n"
                "Как это работает:\n"
                "1. Регистрируешься на сайтах ниже.\n"
                "2. В личном кабинете находишь раздел «Партнерская программа».\n"
                "3. Берешь свою ссылку и отправляешь друзьям.\n\n"
                "💰 <b>Твой доход:</b>\n"
                "Ты получаешь % от заработка друзей.\n"
                "А на этих сайтах есть <b>2 уровня рефералов</b>!\n"
                "Это значит, что ты получаешь % даже с тех, кого привели твои друзья!\n\n"
                "👇 <b>Где брать ссылки:</b>"
            )
            markup = types.InlineKeyboardMarkup()

            # Перебираем все сайты
            for site in sites:
                # Если у сайта есть пометка is_partner - выводим кнопку
                if site.get('is_partner'):
                    btn = types.InlineKeyboardButton(text=f"🔑 {site['name']}", url=site['link'])
                    markup.add(btn)

            btn_back = types.InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_start")
            markup.add(btn_back)

            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='HTML', reply_markup=markup)

        elif call.data == "back_to_start":
            text = "👋 Главное меню..."
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn_catalog = types.InlineKeyboardButton("🗂 Каталог", callback_data="open_catalog")
            markup.add(btn_catalog)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='HTML', reply_markup=markup)

    print("Основной бот (KarmanCash) запущен...")
    bot.infinity_polling()


# --- ГЛАВНЫЙ ЗАПУСК ---
if __name__ == '__main__':
    # Запускаем Основного бота в отдельном потоке
    t_main = threading.Thread(target=run_main_bot)
    t_main.start()

    # Запускаем Входных ботов
    t_zatoon = threading.Thread(target=run_gateway_bot, args=(os.getenv('TOKEN_ZATOON'), comments_zatoon, "Zatoon_bot"))
    t_plus = threading.Thread(target=run_gateway_bot, args=(os.getenv('TOKEN_PLUS'), comments_plus, "PlusRubBot"))
    t_cash = threading.Thread(target=run_gateway_bot, args=(os.getenv('TOKEN_CASH'), comments_cash, "CashKarmanBot"))

    if os.getenv('TOKEN_ZATOON'): t_zatoon.start()
    if os.getenv('TOKEN_PLUS'): t_plus.start()
    if os.getenv('TOKEN_CASH'): t_cash.start()

    print("=== ВСЕ БОТЫ ЗАПУЩЕНЫ ===")
