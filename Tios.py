import telebot
from telebot import types
import time
import requests
from datetime import datetime, timedelta
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
user_data = {}

# Обновленные данные для бота
LEVELS = {
    '📕Магистратура': [
        'Информационные системы и технологии (Информационные системы и технологии)',
        'Конструирование изделий легкой промышленности (Конструирование швейных изделий)',
        'Экономика (Экономика фирмы)',
        'Сервис (Сервис транспортных средств, энергетического оборудования)',
        'Технология изделий легкой промышленности (Технология швейных изделий)',
        'Менеджмент (Стратегическое управление)'
    ],
    '📙Бакалавриат': [
        'Информационные системы и технологии (Информационные системы и технологии)',
        'Радиотехника (Бытовая радиоэлектронная аппаратура)',
        'Инфокоммуникационные технологии и системы связи (Системы мобильной связи)',
        'Технологические машины и оборудование (Бытовые машины и приборы)',
        'Техносферная безопасность (Управление промышленной безопасностью и охраной труда)',
        'Технология изделий легкой промышленности (Технология швейных изделий)',
        'Конструирование изделий легкой промышленности (Конструирование швейных изделий)',
        'Экономика (Финансы и кредит, Экономика предприятий и организаций, бухгалтерский учет, анализ и аудит)',
        'Менеджмент (Менеджмент организации)',
        'Сервис (Сервис транспортных средств, энергетического оборудования и энергоаудит, сервис на предприятиях питания)',
        'Туризм (Технология и организация туроператорских и турагентских услуг)'
    ],
    '📗СПО': [
        'Информационные системы и программирование (на базе основного общего образования)',
        'Информационные системы и программирование (на базе среднего общего образования)',
        'Экономика и бухгалтерский учёт (на базе среднего общего образования)',
        'Экономика и бухгалтерский учёт (на базе основного общего образования)'
    ]
}

# Стоимость обучения по направлениям
COSTS = {
    "📙Бакалавриат": {
        "Экономика (Финансы и кредит, Экономика предприятий и организаций, бухгалтерский учет, анализ и аудит)": {
            "Очная": "122500 рублей",
            "Очно-заочная": "43600 рублей",
            "Заочная": "29900 рублей"
        },
        "Менеджмент (Менеджмент организации)": {
            "Очная": "122500 рублей",
            "Очно-заочная": "43600 рублей",
            "Заочная": "29900 рублей"
        },
        "Сервис (Сервис транспортных средств, энергетического оборудования и энергоаудит, сервис на предприятиях питания)": {
            "Очная": "122500 рублей",
            "Заочная": "29900 рублей"
        },
        "Туризм (Технология и организация туроператорских и турагентских услуг)": {
            "Заочная": "29900 рублей"
        },
        "Информационные системы и технологии (Информационные системы и технологии)": {
            "Очная": "139600 рублей",
            "Очно-заочная": "43600 рублей",
            "Заочная": "29900 рублей"
        },
        "Инфокоммуникационные технологии и системы связи (Системы мобильной связи)": {
            "Очная": "139600 рублей",
            "Заочная": "29900 рублей"
        },
        "Радиотехника (Бытовая радиоэлектронная аппаратура)": {
            "Очная": "139600 рублей",
            "Заочная": "29900 рублей"
        },
        "Техносферная безопасность (Управление промышленной безопасностью и охраной труда)": {
            "Очная": "139600 рублей",
            "Заочная": "29900 рублей"
        },
        "Технология изделий легкой промышленности (Технология швейных изделий)": {
            "Заочная": "29900 рублей"
        },
        "Технологические машины и оборудование (Бытовые машины и приборы)": {
            "Заочная": "29900 рублей"
        },
        "Конструирование изделий легкой промышленности (Конструирование швейных изделий)": {
            "Очная": "139600 рублей",
            "Очно-заочная": "43600 рублей",
            "Заочная": "29900 рублей"
        }
    },
    "📕Магистратура": {
        "Информационные системы и технологии (Информационные системы и технологии)": {
            "Очная": "149400 рублей",
            "Очно-заочная": "50500 рублей",
            "Заочная": "39400 рублей"
        },
        "Технология изделий легкой промышленности (Технология швейных изделий)": {
            "Заочная": "39400 рублей"
        },
        "Конструирование изделий легкой промышленности (Конструирование швейных изделий)": {
            "Заочная": "39400 рублей"
        },
        "Экономика (Экономика фирмы)": {
            "Очная": "132200 рублей",
            "Очно-заочная": "50500 рублей",
            "Заочная": "39400 рублей"
        },
        "Менеджмент (Стратегическое управление)": {
            "Очная": "132200 рублей",
            "Очно-заочная": "50500 рублей",
            "Заочная": "39400 рублей"
        },
        "Сервис (Сервис транспортных средств, энергетического оборудования)": {
            "Очная": "132200 рублей",
            "Заочная": "39400 рублей"
        }
    },
    "📗СПО": {
        "Информационные системы и программирование (на базе основного общего образования)": {
            "Очная": "86400 рублей"
        },
        "Информационные системы и программирование (на базе среднего общего образования)": {
            "Очная": "86400 рублей"
        },
        "Экономика и бухгалтерский учёт (на базе среднего общего образования)": {
            "Очная": "85300 рублей",
            "Заочная": "21900 рублей"
        },
        "Экономика и бухгалтерский учёт (на базе основного общего образования)": {
            "Очная": "85300 рублей",
            "Заочная": "21900 рублей"
        }
    }
}

CONTACT_INFO = """
<b>🏫Контакты приемной комиссии:</b>
📍 Адрес: г. Ставрополь, пр. Кулакова, 41/1, каб. 110
📞 Телефон: 8 (8652) 39-69-97
🕒 Часы работы: 
Пн-Пт: 8:00-17:00 (перерыв 12:00-13:00)
Сб: 9:00-14:00
🌐 Сайт: https://stis.su
📧 Email: otcom@stis.su
"""

ABOUT_UNI = """
<b>🎓 Технологический институт сервиса (ТИС)</b> - филиал Донского государственного технического университета (ДГТУ) в Ставрополе!

🌟 <b>Наши преимущества:</b>
✅ <b>Государственный диплом</b> ДГТУ Ростова-на-Дону
🤝 <b>Стажировки</b> в партнёрских корпорациях ведущего опорного вуза Юга России
💼 <b>Трудоустройство</b> уже на 3-4 курсе

🔮 <b>Перспективные направления:</b>
👨‍💻 IT-технологии
🔧 Сервис и инженерия
📊 Экономика и менеджмент
🎨 Дизайн и конструирование

💫 <b>Стань частью ДГТУ</b> - создавай своё будущее вместе с нами!
🚀 Выбирай престижное образование с гарантией успешной карьеры!
"""


def get_moscow_time():
    moscow_time = datetime.utcnow() + timedelta(hours=3)
    return moscow_time.strftime("%H:%M:%S %d.%m.%Y")


# Функция для получения списка документов по уровню образования
def get_documents_list(level):
    return (
        "\n\n<b>📄 Перечень документов, необходимых для поступления:</b>\n"
        "- Фотография 3x4\n"
        "- Копия паспорта\n"
        "- СНИЛС\n"
        "- Копия ПС или военного билета\n"
    )


def create_inline_keyboard(items, row_width=2, back_button=False, home_button=False):
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    buttons = []

    for item in items:
        if isinstance(item, tuple) and len(item) == 2:
            text, callback_data = item
            buttons.append(types.InlineKeyboardButton(
                text=text, callback_data=callback_data))
        else:
            buttons.append(types.InlineKeyboardButton(
                text=item, callback_data=item))

    for i in range(0, len(buttons), row_width):
        markup.add(*buttons[i:i+row_width])

    extra_buttons = []
    if back_button:
        extra_buttons.append(types.InlineKeyboardButton(
            text="⬅Назад", callback_data="back"))
    if home_button:
        extra_buttons.append(types.InlineKeyboardButton(
            text="🏠На главную", callback_data="home"))

    if extra_buttons:
        markup.add(*extra_buttons)

    return markup


# Главные меню
main_menu_buttons = [
    ("📄Информация для поступающих", "info_for_applicants"),
    ("📞Контактная информация", "contact_info")
]

edu_menu_buttons = [
    ("📕Магистратура", "level_magistr"),
    ("📙Бакалавриат", "level_bakalavr"),
    ("📗СПО", "level_spo"),
    ("О Вузе", "about_uni")
]

finance_menu_buttons = [
    ("💰Бюджет", "finance_budget"),
    ("💵Коммерция", "finance_commercial")
]


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"step": "main_menu"}

    text = f"Привет, {message.from_user.first_name}! Чем могу помочь?"
    markup = create_inline_keyboard(main_menu_buttons, row_width=1)

    bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(commands=['time'])
def send_moscow_time(message):
    time_str = get_moscow_time()
    bot.send_message(
        message.chat.id,
        f"⏰ Текущее московское время:\n<b>{time_str}</b>",
        parse_mode='HTML'
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    new_markup = None
    new_text = call.message.text

    # Обработка навигации
    if data == "info_for_applicants":
        user_data[chat_id] = {"step": "edu_menu"}
        new_text = "Выберите уровень образования:"
        new_markup = create_inline_keyboard(
            edu_menu_buttons, row_width=2, back_button=True)

    elif data == "contact_info":
        user_data[chat_id] = {"step": "contacts"}
        new_text = CONTACT_INFO
        new_markup = create_inline_keyboard(
            [], back_button=False, home_button=True)

    elif data == "about_uni":
        user_data[chat_id] = {"step": "about"}
        new_text = ABOUT_UNI
        new_markup = create_inline_keyboard(
            [], back_button=True, home_button=True)

    elif data.startswith("level_"):
        level_type = data.split("_")[1]
        level_map = {
            "magistr": "📕Магистратура",
            "bakalavr": "📙Бакалавриат",
            "spo": "📗СПО"
        }
        level_name = level_map.get(level_type)

        if level_name:
            user_data[chat_id] = {
                "step": "directions",
                "level": level_name
            }
            new_text = f"Вы выбрали: {level_name}\nВыберите направление:"

            directions = []
            for i, direction in enumerate(LEVELS[level_name]):
                callback_data = f"direction_{level_type}_{i}"
                directions.append((direction, callback_data))

            new_markup = create_inline_keyboard(
                directions, row_width=1, back_button=True, home_button=True)

    elif data.startswith("direction_"):
        parts = data.split('_')
        if len(parts) >= 3:
            level_type = parts[1]
            direction_idx = int(parts[2])
            level_map = {
                "magistr": "📕Магистратура",
                "bakalavr": "📙Бакалавриат",
                "spo": "📗СПО"
            }
            level_name = level_map.get(level_type)

            if level_name and direction_idx < len(LEVELS[level_name]):
                direction_name = LEVELS[level_name][direction_idx]

                user_data[chat_id] = {
                    "step": "finance",
                    "level": level_name,
                    "direction": direction_name
                }
                
                # Для СПО меняем название на "Специальность"
                if level_name == "📗СПО":
                    new_text = f"Специальность: {direction_name}\nВыберите основу обучения:"
                else:
                    new_text = f"Направление: {direction_name}\nВыберите основу обучения:"
                    
                new_markup = create_inline_keyboard(
                    finance_menu_buttons, row_width=2, back_button=True, home_button=True)

    elif data.startswith("finance_"):
        if "direction" in user_data.get(chat_id, {}):
            finance_type = data.split("_")[1]
            finance_name = "💰Бюджет" if finance_type == "budget" else "💵Коммерция"

            data_dict = user_data[chat_id]
            level = data_dict['level']
            direction = data_dict['direction']

            # Для СПО меняем название на "Специальность"
            level_label = "Специальность" if level == "📗СПО" else "Направление"
            
            # Формируем базовую информацию о выборе
            response = (
                f"<b>Ваш выбор:</b>\n"
                f"• Уровень: {level}\n"
                f"• {level_label}: {direction}\n"
                f"• Основа: {finance_name}\n\n"
            )

            # Добавляем информацию о стоимости для коммерческой основы
            if finance_type == "commercial":
                if level in COSTS and direction in COSTS[level]:
                    costs_for_direction = COSTS[level][direction]
                    response += "💸 <b>Стоимость обучения за год:</b>\n\n"
                    for form, cost in costs_for_direction.items():
                        response += f"📑{form}: {cost}\n"
                    response += "\n💡 <b>Оплата возможна по семестрам</b>\n\n"
                else:
                    response += "💸 <b>Стоимость обучения:</b> уточняйте в приемной комиссии\n\n"
                    response += "💡 <b>Оплата возможна по семестрам</b>\n\n"

            # Добавляем информацию о формах обучения для магистратуры
            if level == "📕Магистратура":
                # Обработка бюджетных мест
                if finance_type == "budget":
                    # Направления с бюджетными местами
                    if direction == "Информационные системы и технологии (Информационные системы и технологии)":
                        response += (
                            "📈Минимальный проходной балл: 20\n\n"
                            "📑Очная - 2 года\n"
                            "Всего мест: уточняйте в приемной комиссии\n\n"
                            "📃Очно-заочная – 2,5 года\n"
                            "Всего мест - уточняйте в приемной комиссии\n\n"
                            "📄Заочная – 2.5 года\n"
                            "Всего мест - 3 (уточняйте в приемной комиссии)\n\n"
                        )
                    elif direction == "Конструирование изделий легкой промышленности (Конструирование швейных изделий)":
                        response += (
                            "📈Минимальный проходной балл: 20\n\n"
                            "📑Очная - 2 года\n"
                            "Всего мест: 3 (уточняйте в приемной комиссии)\n\n"
                            "📃Очно-заочная – 2,5 года\n"
                            "Всего мест - уточняйте в приемной комиссии\n\n"
                            "📄Заочная – 2.5 года\n"
                            "Всего мест - уточняйте в приемной комиссии\n\n"
                        )
                    elif direction == "Сервис (Сервис транспортных средств, энергетического оборудования)":
                        response += (
                            "📈Минимальный проходной балл: 20\n\n"
                            "📑Очная - 2 года\n"
                            "Всего мест - 10 (уточняйте в приемной комиссии)\n\n"
                            "📃Очно-заочная – 2,5 года\n"
                            "Всего мест - - (уточняйте в приемной комиссии)\n\n"
                            "📄Заочная – 2.5 года\n"
                            "Всего мест - 10 (уточняйте в приемной комиссии)\n\n"
                        )
                    else:
                        # Для остальных направлений магистратуры
                        response += "⚠️ В этом году бюджетных мест нет.\n\n"
                        new_text = response
                        new_markup = create_inline_keyboard(
                            [], back_button=True, home_button=True)
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=new_text,
                            reply_markup=new_markup,
                            parse_mode='HTML'
                        )
                        return

                # Общая информация для магистратуры
                response += (
                    "📅 <b>Начало приема документов:</b> с 20 июня по 20 августа\n"
                    "📝 <b>Дата проведения вступительных испытаний:</b> "
                )

                if finance_type == "budget":
                    response += "с 21 июня по 15 августа\n"
                    response += "📋 <b>Публикация списков:</b> 26 августа\n\n"
                    response += (
                        "🖋 <b>Завершение предоставления согласия на зачисление:</b>\n"
                        "   24 августа до 12:00 (основной этап зачисления)\n"
                        "✅ <b>Издание приказа о зачислении:</b> 29 августа\n\n"
                    )
                else:
                    response += "с 21 июня по 30 августа\n"
                    response += "📋 <b>Публикация списков:</b> Ежедневно\n\n"
                    response += (
                        "🖋 <b>Завершение предоставления согласия на зачисление:</b>\n"
                        "   За день до приказа\n"
                        "✅ <b>Издание приказа о зачислении:</b> с 01 июля по 30 сентября\n\n"
                    )

                response += "📚 <b>Вступительные испытания:</b> Междисциплинарный экзамен по направлению"

            # Добавляем информацию о формах обучения для бакалавриата
            elif level == "📙Бакалавриат":
                # Обработка бюджетных мест
                if finance_type == "budget":
                    # Для конструкторского направления бюджетных мест нет
                    if direction == "Конструирование изделий легкой промышленности (Конструирование швейных изделий)":
                        response += "⚠️ В этом году бюджетных мест нет.\n\n"
                        new_text = response
                        new_markup = create_inline_keyboard(
                            [], back_button=True, home_button=True)
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=new_text,
                            reply_markup=new_markup,
                            parse_mode='HTML'
                        )
                        return
                    else:
                        # Формируем информацию о местах
                        places_info = ""
                        if direction == "Информационные системы и технологии (Информационные системы и технологии)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - 5 (уточняйте в приемной комиссии)\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 4 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Радиотехника (Бытовая радиоэлектронная аппаратура)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: 7 (уточняйте в приемной комиссии)\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 10 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Инфокоммуникационные технологии и системы связи (Системы мобильной связи)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: 7 (уточняйте в приемной комиссии)\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 15 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Технологические машины и оборудование (Бытовые машины и приборы)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 5 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Техносферная безопасность (Управление промышленной безопасностью и охраной труда)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 6 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Технология изделий легкой промышленности (Технология швейных изделий)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 4 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Экономика (Финансы и кредит, Экономика предприятий и организаций, бухгалтерский учет, анализ и аудит)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - 1 (уточняйте в приемной комиссии)\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                            )
                        elif direction == "Менеджмент (Менеджмент организации)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - 1 (уточняйте в приемной комиссии)\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                            )
                        elif direction == "Сервис (Сервис транспортных средств, энергетического оборудования и энергоаудит, сервис на предприятиях питания)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 14 (уточняйте в приемной комиссии)\n\n"
                            )
                        elif direction == "Туризм (Технология и организация туроператорских и турагентских услуг)":
                            places_info = (
                                "📑Очная - 4 года\n"
                                "Всего мест: уточняйте в приемной комиссии\n\n"
                                "📃Очно-заочная – 4,5 года\n"
                                "Всего мест - уточняйте в приемной комиссии\n\n"
                                "📄Заочная – 4.5 года\n"
                                "Всего мест - 15 (уточняйте в приемной комиссии)\n\n"
                            )

                        response += "📈Минимальный проходной балл на основу обучения:\n\n" + places_info

                # Информация для бакалавриата
                if finance_type == "budget":
                    response += (
                        "📅 <b>Начало приема документов:</b> с 20 июня по 20, 25 июля (Уточняйте в приёмной комиссии)\n\n"
                        "📝 <b>Дата проведения вступительных испытаний:</b> с 21 июня по 25 июля\n\n"
                        "📋 <b>Публикация конкурсных списков:</b> 27 июля\n\n"
                        "🖋 <b>Завершение предоставления согласия на зачисление:</b>\n"
                        "   • 1 августа до 12:00 - на этапе приоритетного зачисления поступающих без вступительных испытаний, а также поступающих на места в пределах квот\n"
                        "   • 5 августа до 12:00 - на основном этапе зачисления, поступающих по результатам вступительных испытаний на основе места в рамках контрольных цифр приема\n\n"
                        "✅ <b>Издание приказа о зачислении:</b>\n"
                        "   • 2 - 3 августа - этап приоритетного зачисления\n\n"
                        "📚 <b>Вступительные испытания:</b> —"
                    )
                else:
                    response += (
                        "📅 <b>Начало приема документов:</b> с 20 июня по 20 августа\n\n"
                        "🌐 <b>Начало приёма документов с помощью суперсервиса \"Поступление в ВУЗ онлайн\":</b> 20 июня\n\n"
                        "📝 <b>Дата проведения вступительных испытаний:</b> с 21 июня по 23 августа\n\n"
                        "📋 <b>Публикация списков:</b> Ежедневно\n\n"
                        "🖋 <b>Завершение предоставления согласия на зачисление:</b> За день до приказа\n\n"
                        "✅ <b>Издание приказа о зачислении:</b> с 21 июня по 30 сентября\n\n"
                        "📚 <b>Вступительные испытания:</b> —"
                    )

            # Обработка для СПО
            elif level == "📗СПО":
                # Обработка бюджетных мест
                if finance_type == "budget":
                    # Специальный вывод для конкретной специальности на бюджет
                    if direction == "Информационные системы и программирование (на базе основного общего образования)":
                        response = (
                            "<b>Ваш выбор:</b>\n"
                            "• Уровень: 📗СПО\n"
                            "• Специальность: Информационные системы и программирование (на базе основного общего образования)\n"
                            "• Основа: 💰Бюджет\n\n"
                            
                            "📑Очная - 2,5 года\n"
                            "Всего мест: 10 (уточняйте в приемной комиссии)\n\n"
                            
                            "📅 Начало приема документов: с 20 июня по 15 августа\n\n"
                            "📋 Публикация конкурсных списков:\n"
                            "15 августа\n\n"
                            "🖋 Завершение приема оригинала об образовании:\n"
                            "15 августа\n\n"
                            "✅ Издание приказа о зачислении:\n"
                            "16 августа\n\n"
                            "📚 Вступительные испытания: Конкурс аттестатов\n"
                        )
                    else:
                        response += "⚠️ В этом году бюджетных мест нет.\n\n"
                        new_text = response
                        new_markup = create_inline_keyboard(
                            [], back_button=True, home_button=True)
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=new_text,
                            reply_markup=new_markup,
                            parse_mode='HTML'
                        )
                        return

                # Обработка коммерческих мест
                elif finance_type == "commercial":
                    if direction == "Информационные системы и программирование (на базе основного общего образования)":
                        response += (
                            "📑Очная - 2,5 года\n"
                            "Всего мест: 15 (уточняйте в приемной комиссии)\n\n"
                        )
                    elif direction == "Информационные системы и программирование (на базе среднего общего образования)":
                        response += (
                            "📑Очная - 2,5 года\n"
                            "Всего мест: 10 (уточняйте в приемной комиссии)\n\n"
                        )
                    elif direction == "Экономика и бухгалтерский учёт (на базе среднего общего образования)":
                        response += (
                            "📑Очная - 2,5 года\n"
                            "Всего мест: 15 (уточняйте в приемной комиссии)\n\n"
                            "📄Заочная – 3.5 года\n"
                            "Всего мест - 10 (уточняйте в приемной комиссии)\n\n"
                        )
                    elif direction == "Экономика и бухгалтерский учёт (на базе основного общего образования)":
                        response += (
                            "📑Очная - 2,5 года\n"
                            "Всего мест: 10 (уточняйте в приемной комиссии)\n\n"
                            "📄Заочная – 3.5 года\n"
                            "Всего мест - 10 (уточняйте в приемной комиссии)\n\n"
                        )
                    else:
                        response += "⚠️ В этом году коммерческих мест нет.\n\n"
                        new_text = response
                        new_markup = create_inline_keyboard(
                            [], back_button=True, home_button=True)
                        bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=message_id,
                            text=new_text,
                            reply_markup=new_markup,
                            parse_mode='HTML'
                        )
                        return

                # Общая информация для СПО (только если не специальный случай)
                if not (finance_type == "budget" and direction == "Информационные системы и программирование (на базе основного общего образования)"):
                    response += (
                        "📅 <b>Начало приема документов:</b> с 20 июня по 15 августа\n\n"
                        "📋 <b>Публикация конкурсных списков:</b>\n"
                    )

                    if finance_type == "budget":
                        response += "15 августа\n\n"
                    else:
                        response += "Ежедневно\n\n"

                    response += (
                        "🖋 <b>Завершение приема оригинала об образовании:</b>\n"
                    )

                    if finance_type == "budget":
                        response += "15 августа\n\n"
                    else:
                        response += "За день до приказа\n\n"

                    response += (
                        "✅ <b>Издание приказа о зачислении:</b>\n"
                    )

                    if finance_type == "budget":
                        response += "16 августа\n\n"
                    else:
                        response += "с 21 июня по 31 августа\n\n"

                    response += "📚 <b>Вступительные испытания:</b> Конкурс аттестатов"
            
            # ДОБАВЛЕНО: Добавляем список документов в конец ответа
            response += get_documents_list(level)
            
            new_text = response
            # Добавляем кнопки "Назад" и "На главную"
            new_markup = create_inline_keyboard(
                [], back_button=True, home_button=True)

    elif data == "back":
        current_step = user_data.get(chat_id, {}).get("step", "main_menu")

        if current_step == "edu_menu":
            user_data[chat_id] = {"step": "main_menu"}
            new_text = "Главное меню"
            new_markup = create_inline_keyboard(main_menu_buttons, row_width=1)

        elif current_step == "directions":
            user_data[chat_id] = {"step": "edu_menu"}
            new_text = "Выберите уровень образования:"
            new_markup = create_inline_keyboard(
                edu_menu_buttons, row_width=2, back_button=True)

        elif current_step == "finance":
            # Возврат к выбору направления
            level = user_data[chat_id].get("level", "")
            if level:
                user_data[chat_id] = {
                    "step": "directions",
                    "level": level
                }
                new_text = f"Вы выбрали: {level}\nВыберите направление:"
                directions = []
                level_type = ""
                if level == "📕Магистратура":
                    level_type = "magistr"
                elif level == "📙Бакалавриат":
                    level_type = "bakalavr"
                elif level == "📗СПО":
                    level_type = "spo"

                if level_type:
                    for i, direction in enumerate(LEVELS[level]):
                        callback_data = f"direction_{level_type}_{i}"
                        directions.append((direction, callback_data))

                    new_markup = create_inline_keyboard(
                        directions, row_width=1, back_button=True, home_button=True)

        elif current_step in ["contacts", "about"]:
            user_data[chat_id] = {"step": "edu_menu"}
            new_text = "Выберите уровень образования:"
            new_markup = create_inline_keyboard(
                edu_menu_buttons, row_width=2, back_button=True)

    elif data == "home":
        user_data[chat_id] = {"step": "main_menu"}
        new_text = "Главное меню"
        new_markup = create_inline_keyboard(main_menu_buttons, row_width=1)

    # Обновляем сообщение
    if new_markup:
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text,
                reply_markup=new_markup,
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
    else:
        bot.answer_callback_query(call.id, "Действие не найдено")


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {"step": "main_menu"}

    bot.send_message(
        chat_id,
        "Пожалуйста, используйте интерактивные кнопки для навигации",
        reply_markup=create_inline_keyboard(main_menu_buttons, row_width=1)
    )


if __name__ == '__main__':
    print(f"🟢 [{get_moscow_time()}] Бот для абитуриентов вуза запущен")

    while True:
        try:
            print(f"🟢 [{get_moscow_time()}] Бот активен и ожидает сообщения...")
            bot.polling(none_stop=True, timeout=30)

        except requests.exceptions.ConnectionError:
            error_time = get_moscow_time()
            print(
                f"🔴 [{error_time}] Ошибка соединения. Перезапуск через 15 сек...")
            time.sleep(15)

        except Exception as e:
            error_time = get_moscow_time()
            print(f"⚠️ [{error_time}] Критическая ошибка: {e}")
            print(f"⚠️ [{error_time}] Перезапуск бота через 30 секунд...")
            time.sleep(30)