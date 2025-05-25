# Добавить аккаунт тг
# Добавить бота
# Добавить отслеживаемый чат
# Настроить наблюдение
# Настроить репостинг
# Настроить генерацию тестов
# Инструкция

from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def keyboard_main():
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
    builder.add(
        InlineKeyboardButton(
            text="Добавить бота",
            callback_data="add_bot"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Добавить чат",
            callback_data="add_tracked_chat"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Настроить наблюдение",
            callback_data="setup_monitoring"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Настроить репостинг",
            callback_data="setup_reposting"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Настроить генерацию тестов",
            callback_data="setup_test_generation"
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Инструкция",
            callback_data="show_instructions"
        )
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

    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()


def keyboards_cancellation():
    keyboards = [[InlineKeyboardButton(text="❌ отмена ввода данных", callback_data="keyboard_remover")]]

    service = InlineKeyboardMarkup(inline_keyboard=keyboards,
                                  )
    return service