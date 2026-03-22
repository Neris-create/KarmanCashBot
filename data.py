import os

# --- БАЗА ДАННЫХ САЙТОВ ---
sites = []

def init_data():
    sites.clear()

    # Загружаем ссылки
    link_unu = os.getenv('UNU_LINK', 'https://unu.im')
    link_soc = os.getenv('SOC_PUBLIC', 'https://socpublic.com')
    link_mj = os.getenv('MJ_PUBLIC', 'https://mjpublic.com')
    link_task = os.getenv('TASK_PAY', 'https://taskpay.ru')

    # --- UNU ---
    sites.append({
        "id": 0,
        "name": "🔥 UNU (Выбор редакции)",
        "desc": (
            "📌 <b>О чем:</b> Комментарии, отзывы, активность.\n"
            "💰 <b>Цена задания:</b> от 3₽ до 20₽.\n"
            "💸 <b>Мин. вывод:</b> от 100₽.\n"
            "🏦 <b>Куда выводят:</b>\n"
            "• Банковская карта (РФ) — от 200₽\n"
            "• СБП — от 100₽\n"
            "• ЮMoney — от 100₽\n\n"

            "⚡️ <b>Вердикт:</b> Лучший старт для новичков. Быстрый вывод."
        ),
        "link": link_unu,
        "button_text": "Перейти на UNU"
    })

    # --- Socpublic ---
    sites.append({
        "id": 1,
        "name": "🔵 Socpublic",
        "desc": (
             "📌 <b>О чем:</b> Лайки, репосты, подписки в соцсетях.\n"
            "💰 <b>Цена задания:</b> от 0.30₽ до 5₽.\n"
            "💸 <b>Мин. вывод:</b> от 11₽.\n"
            "🏦 <b>Куда выводят:</b>\n"
            "• Банковская карта (РФ) — от 145₽\n"
            "• Банковская карта (НЕ РФ) — от 400₽\n"
            "• СБП — от 50₽\n"
            "• Номер мобильного телефона — от 50₽\n"
            "• WebMoney WMT — от 11₽\n"
            "• WebMoney WMZ — от 11₽\n"
            "• USDT TRC-20 — от 700₽\n\n"

            "⚡️ <b>Вердикт:</b> Самый надежный старичок. Минимальный вывод на любой тапочек."
        ),
        "link": link_soc,
        "button_text": "Перейти на Socpublic",
        "is_partner": True
    })

    # --- MJ Public ---
    sites.append({
        "id": 2,
        "name": "🟣 MJ Public",
        "desc": (
             "📌 <b>О чем:</b> Накрутка и активность в соцсетях.\n"
            "💰 <b>Цена задания:</b> от 0.50₽ до 10₽.\n"
            "💸 <b>Мин. вывод:</b> от 300₽.\n"
            "🏦 <b>Куда выводят:</b>\n"
            "• СБП — от 300₽\n\n"

            "⚡️ <b>Вердикт:</b> Хорош для разнообразия. "
        ),
        "link": link_mj,
        "button_text": "Перейти на MJ Public"
    })

    # --- TaskPay ---
    sites.append({
        "id": 3,
        "name": "🟠 TaskPay",
        "desc": (
             "📌 <b>О чем:</b> Тестирование приложений, отзывы, лайки.\n"
            "💰 <b>Цена задания:</b> от 5₽ до 50₽.\n"
            "💸 <b>Мин. вывод:</b> от 100₽.\n"
            "🏦 <b>Куда выводят:</b>\n"
            "• Банковская карта — от 100₽\n"
            "• Volet (RUB) — от 100₽\n\n"

            "⚡️ <b>Вердикт:</b> Задания сложнее, но плата выше."
        ),
        "link": link_task,
        "button_text": "Перейти на TaskPay",
        "is_partner": True
    })
