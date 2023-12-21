from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram import types


def get_keyboard_find_buyer():
    """Инлайн кнопки если покупатель найден"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Обращение по гарантии", callback_data="warranty"
    )
    builder.button(
        text="Зарегистрировать продажу", callback_data="sale"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_key_cancel():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    return builder.as_markup()


def get_keyboard_not_find_duyer():
    """Инлайн кнопки если покупатель не найден"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить", callback_data="add"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_save_and_cancel():
    """Инлайн кнопки отменить и сохранить"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить", callback_data="add_obj"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_sale_save_and_cancel():
    """Инлайн кнопки провести продажу и отменить"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Провести продажу", callback_data="sale_save"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_warranty_save_and_cancel():
    """Инлайн кнопки отменить и сохранить"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить", callback_data="upd_obj"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keybords_add_del_employee():
    """Кнопки админа"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Добавить продавца", callback_data="add_employee"
    )
    builder.button(
        text="Заблокировать продавца", callback_data="ban_employee"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_yes_no():
    """Инлайн кнопки сделать админом"""
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Дa", callback_data="is_admin_true"
    )
    builder.button(
        text="Нет", callback_data="is_admin_false"
    )
    builder.adjust(2)
    return builder.as_markup()


def repeat():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Продолжить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_save_and_cancel_employee():
    """Инлайн кнопки отменить и сохранить сотрудника"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Сохранить", callback_data="save_employee"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()


def get_keyboard_banned_employee():
    """Инлайн кнопки отменить и сохранить сотрудника"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text="Заблокировать", callback_data="banned_employee"
    )
    builder.button(
        text="Отменить", callback_data="cancel"
    )
    builder.adjust(1)
    return builder.as_markup()