import os

# --- БАЗА ДАННЫХ САЙТОВ ---
# Мы создаем список sites пустым, а потом заполняем его в функции init_data
sites = []

def init_data():
    # Эта функция берет ссылки из переменных окружения (.env)
    # и заполняет список сайтов.
    sites.clear()

    # Получаем ссылки из .env (если ссылки нет, ставим заглушку)
    link_unu = os.getenv('UNU_LINK', 'https://unu.im')
    link_soc = os.getenv('SOC_PUBLIC', 'https://socpublic.com')
    link_mj = os.getenv('MJ_PUBLIC', 'https://mjpublic.com')
    link_task = os.getenv('TASK_PAY', 'https://taskpay.ru')

    sites.append({
        "id": 0,
        "name": "🔥 UNU (Выбор редакции)",
        "desc": (
            "📌 <b>О чем:</b> Комментарии, отзывы, активность.\n"
            "💰 <b>Цена задания:</b> от 3₽ до 20₽.\n"
            "💸 <b>Мин. вывод:</b> от 100₽.\n"
            "🏦 <b>Куда выводят:</b>\n"
            "• СБП — от 100₽\n"
            "• ЮMoney — от 100₽\n\n"
            "⚡️ <b>Вердикт:</b> Лучший старт для новичков."
        ),
        "link": link_unu,
        "button_text": "Перейти на UNU"
    })

    sites.append({
        "id": 1,
        "name": "🔵 Socpublic",
        "desc": (
            "📌 <b>О чем:</b> Лайки, репосты, подписки.\n"
            "💰 <b>Цена:</b> от 0.30₽ до 5₽.\n"
            "💸 <b>Мин. вывод:</b> от 11₽.\n\n"
            "⚡️ <b>Вердикт:</b> Надежный старичок."
        ),
        "link": link_soc,
        "button_text": "Перейти на Socpublic"
    })

    sites.append({
        "id": 2,
        "name": "🟣 MJ Public",
        "desc": (
            "📌 <b>О чем:</b> Накрутка в соцсетях.\n"
            "💰 <b>Цена:</b> от 0.50₽ до 10₽.\n"
            "💸 <b>Мин. вывод:</b> от 300₽.\n\n"
            "⚡️ <b>Вердикт:</b> Для разнообразия."
        ),
        "link": link_mj,
        "button_text": "Перейти на MJ Public"
    })

    sites.append({
        "id": 3,
        "name": "🟠 TaskPay",
        "desc": (
            "📌 <b>О чем:</b> Тестирование приложений.\n"
            "💰 <b>Цена:</b> от 5₽ до 50₽.\n"
            "💸 <b>Мин. вывод:</b> от 100₽.\n\n"
            "⚡️ <b>Вердикт:</b> Плата выше."
        ),
        "link": link_task,
        "button_text": "Перейти на TaskPay"
    })

# Список для раздела "Стать партнером"
partner_sites = [
    {"name": "Socpublic", "link": os.getenv('SOC_PUBLIC')},
    {"name": "TaskPay", "link": os.getenv('TASK_PAY')},
    {"name": "UNU", "link": os.getenv('UNU_LINK')}
]
