from subprocess import \
    Popen, PIPE

from telegram import \
    Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import \
    Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from config import \
    TG_TOKEN, TG_API_URL


# `callback_data` - это то, что будет присылать TG при нажатии на каждую
# кнопку.
# Поэтому каждый идентификатор должен быть уникальным
CALLBACK_BUTTON1_LEFT = "callback_button1_left"
CALLBACK_BUTTON2_RIGHT = "callback_button2_right"
CALLBACK_BUTTON3_MORE = "callback_button3_more"
CALLBACK_BUTTON4_BACK = "callback_button4_back"
CALLBACK_BUTTON5_TIME = "callback_button5_time"
CALLBACK_BUTTON6_PRICE = "callback_button6_price"
CALLBACK_BUTTON7_PRICE = "callback_button7_price"
CALLBACK_BUTTON8_PRICE = "callback_button8_price"


TITLES = {
    CALLBACK_BUTTON1_LEFT: "Новое сообщение ⚡️",
    CALLBACK_BUTTON2_RIGHT: "Отредактировать ✏️",
    CALLBACK_BUTTON3_MORE: "Ещё ➡️",
    CALLBACK_BUTTON4_BACK: "Назад ⬅️",
    CALLBACK_BUTTON5_TIME: "Время ⏰",
    CALLBACK_BUTTON6_PRICE: "BTC 💰",
    CALLBACK_BUTTON7_PRICE: "LTC 💰",
    CALLBACK_BUTTON8_PRICE: "ETH 💰",
}


# Глобально инициализируем клиент API Bittrex
# client = BittrexClient()


def get_base_inline_keyboard():
    """
    Получить клавиатуру для сообщения.
    Эта клавиатура будет видна под каждым сообщением, где ее прикрепили.
    """
    # Каждый список внутри keyboard -- это горизонтальный ряд кнопок
    keyboard = [
        # Каждый элемент внутри списка -- это один вертикальный столбец
        # Сколько кнопок -- столько столбцов
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT],
                                 callback_data=CALLBACK_BUTTON1_LEFT),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT],
                                 callback_data=CALLBACK_BUTTON2_RIGHT),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE],
                                 callback_data=CALLBACK_BUTTON3_MORE),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hello! Send me something",
    )


def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="This is a test bot\n"
             "List of available commands is in the menu\n"
             "Also I can reply on any message",
    )


def do_time(bot: Bot, update: Update):
    """ Check time on server
    """
    process = Popen("date", stdout=PIPE)
    text, error = process.communicate()
    # There might ve an error when process returns 0
    if error:
        text = "There was an error, I cannot provide time"
    else:
        # Decode reply command from process
        text = text.decode("utf-8")

    bot.send_message(
        chat_id=update.message.chat_id,
        text=text,
    )


def do_echo(bot: Bot, update: Update):
    chat_id = update.message.chat_id
    text = f"Your ID = {chat_id}\n\n{update.message.text}"

    bot.send_message(
        chat_id=chat_id,
        text=text,
    )


def main():
    bot = Bot(
        token=TG_TOKEN,
        base_url=TG_API_URL,
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    help_handler = CommandHandler("help", do_help)
    time_handler = CommandHandler("time", do_time)
    message_handler = MessageHandler(Filters.text, do_echo)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(time_handler)
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
