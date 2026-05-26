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
from database import create_db, save_schedule
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


days = get_next_days()

user_data = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("✅ Работаю без выходных", callback_data="full_week")],
        [InlineKeyboardButton("📅 Выбрать выходные", callback_data="choose_days")]
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
        await query.edit_message_text(
            "✅ График отправлен"
)

    elif query.data == "choose_days":

        user_data[user_id] = []

        keyboard = []

        for day in days:
            keyboard.append([
                InlineKeyboardButton(
                day,
                callback_data=f"day|{day}"
            )
         ])

        keyboard.append(
            [InlineKeyboardButton("📨 Отправить", callback_data="send_days")]
        )

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            "Выберите выходные:",
            reply_markup=reply_markup
        )

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

        await query.edit_message_text(
            "✅ График отправлен"
        )

    else:

       if query.data.startswith("day|"):

            selected_day = query.data.split("|")[1]

            if user_id not in user_data:
                user_data[user_id] = []

            if selected_day not in user_data[user_id]:
                user_data[user_id].append(selected_day)

            selected = ", ".join(user_data[user_id])

            await query.answer(
                text=f"Выбрано: {selected}"
            )
create_db()
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Бот запущен...")

app.run_polling()