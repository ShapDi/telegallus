# Добавить аккаунт тг
# Добавить бота
# Добавить отслеживаемый чат
# Настроить наблюдение
# Настроить репостинг
# Настроить генерацию тестов
# Инструкция

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def keyboard_main(user_bot_id):
    """
    Основная клавиатура для управления процессом перерепостинга
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Управление аккаунтами",
            callback_data=f"management_tg_account.{user_bot_id}",
            # add_tg_account
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Настройка чатов", callback_data=f"management_chat_radar.{user_bot_id}"
        )
    )
    # builder.add(
    #     InlineKeyboardButton(
    #         text="Настроика наблюдение",
    #         callback_data="setup_monitoring"
    #     )
    # )
    builder.add(
        InlineKeyboardButton(
            text="Настроить репостинг", callback_data="setup_reposting"
        )
    )
    # builder.add(
    #     InlineKeyboardButton(
    #         text="Настроить генерацию тестов",
    #         callback_data="setup_test_generation"
    #     )
    # )
    builder.add(
        InlineKeyboardButton(text="Инструкция", callback_data="show_instructions")
    )
    builder.adjust(2, 2, 2, 1)  # Распределение кнопок по 2 в ряду, последняя одна
    return builder.as_markup()


def keyboard_add_tg_account(user_bot_id: str):
    """
    Основная клавиатура для управления процессом перерепостинга
    """
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text="Добавить аккаунт тг",
            callback_data="add_tg_account",
        )
    )

    builder.adjust(1, 1, 1, 1, 1)
    return builder.as_markup()


def keyboard_management_tg_account(accounts):
    builder = InlineKeyboardBuilder()

    print(accounts)

    for account in accounts:
        builder.add(
            InlineKeyboardButton(
                text=account.name_account,
                callback_data=f"account.{account.id}",
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="Добавить аккаунт тг",
            callback_data="add_tg_account",
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Вернутся в меню",
            callback_data="keyboard_remover",
        )
    )

    builder.adjust(1, 1, 1, 1, 2)
    return builder.as_markup()


def keyboard_management_bot(bots, account_id, user_id):
    builder = InlineKeyboardBuilder()

    for bot in bots:
        builder.add(
            InlineKeyboardButton(
                text=bot.bot_key_protected,
                callback_data=f"account.{bot.id}",
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="Добавить бота",
            callback_data=f"add_bot.{account_id}",
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"management_tg_account.{user_id}",
        )
    )

    builder.adjust(1, 1, 1, 1, 2)
    return builder.as_markup()


def keyboard_add_bot(bots):
    pass


def keyboard_chat_radars(chat_radars, account_id):
    builder = InlineKeyboardBuilder()

    for chat in chat_radars:
        builder.add(
            InlineKeyboardButton(
                text=chat.name,
                callback_data=f"account.{chat.id}",
            )
        )

    builder.add(
        InlineKeyboardButton(
            text="Добавить чат",
            callback_data=f"add_tracked_chat.{account_id}",
        )
    )

    builder.add(
        InlineKeyboardButton(
            text="Вернутся в меню",
            callback_data="keyboard_remover",
        )
    )

    builder.adjust(1, 1, 1, 1, 2)
    return builder.as_markup()


def keyboards_cancellation():
    keyboards = [
        [
            InlineKeyboardButton(
                text="❌ отмена ввода данных", callback_data="keyboard_remover"
            )
        ]
    ]

    service = InlineKeyboardMarkup(
        inline_keyboard=keyboards,
    )
    return service
