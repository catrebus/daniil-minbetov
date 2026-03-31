from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Сделать ставку за"),
        KeyboardButton(text="Сделать ставку против")
    )
    builder.row(
        KeyboardButton(text="Вывести ставки")
    )
    return builder.as_markup(resize_keyboard=True)