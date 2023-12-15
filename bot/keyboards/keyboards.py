from aiogram.utils.keyboard import InlineKeyboardBuilder


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