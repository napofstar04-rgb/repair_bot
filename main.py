from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import (
    create_db,
    save_schedule,
    save_user,
    get_all_users
)
TOKEN = "8715635323:AAELRdsMlUXrbwfsrLOaWmyms7v9hqkOwUw"
ADMIN_ID = 8626163973

from datetime import datetime, timedelta


def get_next_days(days_count=14):

    result = []

    weekdays = {
        0: "Пн",
        1: "Вт",
        2: "Ср",
        3: "Чт",
        4: "Пт",
        5: "Сб",
        6: "Вс"
    }

    today = datetime.now()

    for i in range(days_count):

        day = today + timedelta(days=i)

        formatted = f"{weekdays[day.weekday()]} {day.strftime('%d.%m')}"

        result.append(formatted)

    return result


DAYS = get_next_days()

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    save_user(user_id)

    keyboard = [

    [
        InlineKeyboardButton(
            "Работаю без выходных",
            callback_data="full_week"
        )
    ],

    [
        InlineKeyboardButton(
            "📅 Выбрать выходные",
            callback_data="choose_days"
        )
    ],

    [
        InlineKeyboardButton(
            "✏️ Изменить выходные",
            callback_data="edit_days"
        )
    ]
]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Здравствуйте! Отправьте ваш график:",
        reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user_id = query.from_user.id

    await query.answer()

    # Работает без выходных
    if query.data == "full_week":

        text = (
            f"📅 Новый график\n\n"
            f"👷 {query.from_user.full_name}\n"
            f"Работает без выходных ✅"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

        save_schedule(
            user_id,
            query.from_user.full_name,
            "Работает без выходных"
        )

        back_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back_menu"
                )
            ]
        ])

        await query.edit_message_text(
            f"✅ График отправлен\n\n"
            f"Ваши выходные:\n{text_days}",
            reply_markup=back_keyboard
        )

    # Выбор выходных
    elif query.data == "choose_days":

        if user_id not in user_data:
            user_data[user_id] = []

        keyboard = []

        for i, day in enumerate(DAYS):
            keyboard.append([
                 InlineKeyboardButton(
                    day,
                    callback_data=f"day_{i}"
                 )
             ])

        keyboard.append([
            InlineKeyboardButton(
                "📨 Отправить",
                callback_data="send_days"
            )
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "Выберите выходные:",
            reply_markup=reply_markup
        )
    elif query.data == "edit_days":

        user_data[user_id] = []

        keyboard = []

        for i, day in enumerate(DAYS):

            keyboard.append([
                InlineKeyboardButton(
                    day,
                    callback_data=f"edit_{i}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "📨 Сохранить новый график",
                callback_data="save_edit_days"
            )
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "Выберите новые выходные:",
            reply_markup=reply_markup
        )

    # Отправка графика
    elif query.data == "send_days":

        selected_days = user_data.get(user_id, [])

        if not selected_days:
            text_days = "без выходных"
        else:
            text_days = ", ".join(selected_days)

        text = (
            f"📅 Новый график\n\n"
            f"👷 {query.from_user.full_name}\n"
            f"Выходные: {text_days}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

        save_schedule(
            user_id,
            query.from_user.full_name,
            text_days
        )

        user_data[user_id] = []

        back_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back_menu"
                )
            ]
        ])

        await query.edit_message_text(
            f"✅ График отправлен\n\n"
            f"Ваши выходные:\n{text_days}",
            reply_markup=back_keyboard
        )
    elif query.data == "save_edit_days":

        selected_days = user_data.get(user_id, [])

        if not selected_days:
            text_days = "без выходных"
        else:
            text_days = ", ".join(selected_days)

        text = (
            f"✏️ График изменён\n\n"
            f"👷 {query.from_user.full_name}\n"
            f"Новые выходные: {text_days}"
        )

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=text
        )

        save_schedule(
            user_id,
            query.from_user.full_name,
            text_days
        )

        user_data[user_id] = []

        back_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back_menu"
                )
            ]
        ])

        await query.edit_message_text(
            f"✅ Новый график сохранён\n\n"
            f"Ваши выходные:\n{text_days}",
            reply_markup=back_keyboard
        )
    elif query.data == "back_menu":

        keyboard = [

            [
                InlineKeyboardButton(
                    "Работаю без выходных",
                    callback_data="full_week"
                )
            ],

            [
                InlineKeyboardButton(
                    "📅 Выбрать выходные",
                    callback_data="choose_days"
                )
            ],

            [
                InlineKeyboardButton(
                    "✏️ Изменить выходные",
                    callback_data="edit_days"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "Выберите вариант:",
            reply_markup=reply_markup
        )
    # Выбор даты
    elif (
        query.data.startswith("day_")
        or query.data.startswith("edit_")
    ):

        day_index = int(query.data.split("_")[1])

        selected_day = DAYS[day_index]

        if user_id not in user_data:
            user_data[user_id] = []

        if selected_day in user_data[user_id]:
            user_data[user_id].remove(selected_day)
        else:
            user_data[user_id].append(selected_day)

        keyboard = []

        is_edit = query.data.startswith("edit_")

        for i, day in enumerate(DAYS):

            if day in user_data[user_id]:
                button_text = f"✅ {day}"
            else:
                button_text = day

            callback_prefix = "edit" if is_edit else "day"

            keyboard.append([
                InlineKeyboardButton(
                    button_text,
                    callback_data=f"{callback_prefix}_{i}"
                )
            ])

        submit_callback = (
            "save_edit_days"
            if is_edit
            else "send_days"
        )

        submit_text = (
            "📨 Сохранить новый график"
            if is_edit
            else "📨 Отправить"
        )

        keyboard.append([
            InlineKeyboardButton(
                submit_text,
                callback_data=submit_callback
            )
        ])

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_reply_markup(
            reply_markup=reply_markup
        )
    async def send_reminders(app):

    users = get_all_users()

    keyboard = [

        [
            InlineKeyboardButton(
                "Работаю без выходных",
                callback_data="full_week"
            )
        ],

        [
            InlineKeyboardButton(
                "📅 Выбрать выходные",
                callback_data="choose_days"
            )
        ],

        [
            InlineKeyboardButton(
                "✏️ Изменить выходные",
                callback_data="edit_days"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    for user in users:

        user_id = user[0]

        try:

            await app.bot.send_message(
                chat_id=user_id,
                text=(
                    "📅 Пора обновить график!\n\n"
                    "Выберите выходные на следующие 2 недели."
                ),
                reply_markup=reply_markup
            )

        except Exception as e:
            print(f"Ошибка отправки {user_id}: {e}")
create_db()
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
scheduler = AsyncIOScheduler()

scheduler.add_job(
    send_reminders,
    "interval",
    minutes=1,
    args=[app]
)

scheduler.start()
print("Бот запущен...")

app.run_polling()