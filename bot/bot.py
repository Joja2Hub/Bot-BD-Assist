import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.session import aiohttp
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from config import BOT_TOKEN
from services import fetch_clients, get_client_by_id, fetch_all_contracts, add_contract, remove_contract, \
    get_contract_by_id, add_client, remove_client

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Основное меню
def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Клиенты", callback_data="clients")],
        [InlineKeyboardButton(text="Контракты", callback_data="contracts")]
    ])

# Клавиатура для клиентов
def clients_keyboard(back_callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Все клиенты", callback_data="all_clients")],
        [InlineKeyboardButton(text="Добавить клиента", callback_data="add_client")],
        [InlineKeyboardButton(text="Удалить клиента", callback_data="remove_client")],
        [InlineKeyboardButton(text="Назад", callback_data=back_callback)]
    ])

# Клавиатура для контракта
def contracts_keyboard(back_callback: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Все контракты", callback_data="all_contracts")],
        [InlineKeyboardButton(text="Добавить контракт", callback_data="add_contract")],
        [InlineKeyboardButton(text="Удалить контракт", callback_data="remove_contract")],
        [InlineKeyboardButton(text="Назад", callback_data=back_callback)]
    ])

# Функция безопасного обновления сообщения
async def safe_edit_message(callback: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup) -> None:
    try:
        await callback.message.edit_text(text=text, reply_markup=reply_markup)
    except Exception as e:
        print(f"Error updating message: {e}")

# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Приветственное сообщение и регистрация/обновление пользователя."""
    telegram_id = message.from_user.id
    name = message.from_user.full_name

    await message.answer(
        text=f"Привет, {name}! Выберите действие:",
        reply_markup=main_menu_keyboard()
    )

# Доступные клиенты
@dp.callback_query(lambda c: c.data == "clients")
async def show_clients_menu(callback: CallbackQuery) -> None:
    await safe_edit_message(
        callback,
        text="Меню клиентов:",
        reply_markup=clients_keyboard(back_callback="main_menu")
    )

# Доступные контракты
@dp.callback_query(lambda c: c.data == "contracts")
async def show_contracts_menu(callback: CallbackQuery) -> None:
    await safe_edit_message(
        callback,
        text="Меню контрактов:",
        reply_markup=contracts_keyboard(back_callback="main_menu")
    )

# Все клиенты
@dp.callback_query(lambda c: c.data == "all_clients")
async def show_all_clients(callback: CallbackQuery) -> None:
    clients = await fetch_clients()  # Получаем список всех клиентов
    clients_buttons = [[InlineKeyboardButton(text=client["name"], callback_data=f"client_{client['id']}")] for client in clients]
    clients_buttons.append([InlineKeyboardButton(text="Назад", callback_data="clients")])

    await safe_edit_message(
        callback,
        text="Все клиенты:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=clients_buttons)
    )

# Все контракты
@dp.callback_query(lambda c: c.data == "all_contracts")
async def show_all_contracts(callback: CallbackQuery) -> None:
    contracts = await fetch_all_contracts()  # Получаем список всех контрактов
    contracts_buttons = [
        [InlineKeyboardButton(text=contract["title"], callback_data=f"contract_{contract['id']}")]  # Используем название контракта
        for contract in contracts
    ]
    contracts_buttons.append([InlineKeyboardButton(text="Назад", callback_data="contracts")])

    await safe_edit_message(
        callback,
        text="Все контракты:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=contracts_buttons)
    )


# Добавить клиента
@dp.callback_query(lambda c: c.data == "add_client")
async def add_new_client(callback: CallbackQuery) -> None:
    await callback.answer("Добавить нового клиента.", show_alert=True)
    # Логика добавления нового клиента
    await callback.message.answer("Введите имя нового клиента:")
    # Ожидаем ответа пользователя
    await dp.storage.set_data(user=callback.from_user.id, data={"action": "add_client_name"})

# Удаление клиента
@dp.callback_query(lambda c: c.data == "remove_client")
async def remove_existing_client(callback: CallbackQuery) -> None:
    """Отображаем список всех клиентов для удаления."""
    clients = await fetch_clients()  # Получаем список всех клиентов
    if not clients:
        await callback.message.answer("Нет доступных клиентов для удаления.")
        return

    # Создаем кнопки для удаления каждого клиента
    clients_buttons = [
        [InlineKeyboardButton(text=client["name"], callback_data=f"delete_client_{client['id']}")]
        for client in clients
    ]
    clients_buttons.append([InlineKeyboardButton(text="Назад", callback_data="clients")])

    # Отправляем сообщение с кнопками
    await safe_edit_message(
        callback,
        text="Выберите клиента для удаления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=clients_buttons)
    )

# Обработчик удаления клиента
@dp.callback_query(lambda c: c.data and c.data.startswith("delete_client_"))
async def delete_client(callback: CallbackQuery) -> None:
    # Логируем данные callback перед извлечением ID
    logger.info(f"Нажата кнопка для удаления клиента. Данные callback: {callback.data}")

    try:
        # Извлекаем ID клиента из callback_data
        client_id = int(callback.data.split("_")[2])
        # Выполняем удаление клиента
        response = await remove_client(client_id)
        if response.get("status") == "success":
            await callback.answer("Клиент был успешно удален.", show_alert=True)
            await fetch_clients()  # Обновление списка клиентов
        else:
            await callback.answer("Не удалось удалить клиента. Попробуйте снова.", show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка при удалении клиента: {e}")
        await callback.answer("Ошибка при удалении клиента. Попробуйте снова.", show_alert=True)



# Добавить контракт
@dp.callback_query(lambda c: c.data == "add_contract")
async def add_new_contract(callback: CallbackQuery) -> None:
    await callback.answer("Добавить новый контракт.", show_alert=True)
    # Логика добавления нового контракта

# Удаление контракта
@dp.callback_query(lambda c: c.data == "remove_contract")
async def remove_existing_contract(callback: CallbackQuery) -> None:
    """Отображаем список всех контрактов для удаления."""
    contracts = await fetch_all_contracts()  # Получаем список всех контрактов
    if not contracts:
        await callback.message.answer("Нет доступных контрактов для удаления.")
        return

    # Создаем кнопки для удаления каждого контракта
    contracts_buttons = [
        [InlineKeyboardButton(text=f"Контракт {contract['id']}", callback_data=f"delete_contract_{contract['id']}")]
        for contract in contracts
    ]
    contracts_buttons.append([InlineKeyboardButton(text="Назад", callback_data="contracts")])

    # Отправляем сообщение с кнопками
    await safe_edit_message(
        callback,
        text="Выберите контракт для удаления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=contracts_buttons)
    )

# Обработчик удаления контракта
@dp.callback_query(lambda c: c.data and c.data.startswith("delete_contract_"))
async def delete_contract(callback: CallbackQuery) -> None:
    """Удаляем контракт по его ID."""
    logger.info(f"Нажата кнопка для удаления контракта. Данные callback: {callback.data}")

    try:
        # Извлекаем ID контракта из callback_data
        contract_id = int(callback.data.split("_")[2])

        # Выполняем удаление контракта
        response = await remove_contract(contract_id)
        if response.get("status") == "success":
            await callback.answer("Контракт был успешно удален.", show_alert=True)
            await remove_existing_contract(callback)  # Обновляем список доступных контрактов
        else:
            await callback.answer("Не удалось удалить контракт. Попробуйте снова.", show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка при удалении контракта: {e}")
        await callback.answer("Ошибка при удалении контракта. Попробуйте снова.", show_alert=True)


# Детали клиента
@dp.callback_query(lambda c: c.data.startswith("client_"))
async def show_client_details(callback: CallbackQuery) -> None:
    client_id = int(callback.data.split("_")[1])
    client = await get_client_by_id(client_id)  # Получаем клиента по ID

    if client:
        # Формируем детали клиента, используя поля из модели
        client_details = (
            f"Клиент: {client['name']}\n"
            f"Контактная информация: {client['contact_info'] if client.get('contact_info') else 'Не указана'}\n"
            f"Дата регистрации: {client['created_at']}\n"
        )

        # Отправляем детали клиента
        await safe_edit_message(
            callback,
            text=client_details,
        )
    else:
        await callback.answer("Клиент не найден.", show_alert=True)



# Детали контракта
@dp.callback_query(lambda c: c.data.startswith("contract_"))
async def show_contract_details(callback: CallbackQuery) -> None:
    contract_id = int(callback.data.split("_")[1])  # Extract contract ID from callback data
    contract = await get_contract_by_id(contract_id)  # Fetch contract details from the backend

    if contract:
        client = await get_client_by_id(contract["client_id"])  # Fetch client details related to the contract

        # Displaying the contract details
        contract_details = (
            f"Контракт {contract['id']}:\n"
            f"Название: {contract['title']}\n"
            f"Id Клиента: {contract['client_id']}\n"
            f"Описание: {contract['description'] if contract['description'] else 'Нет описания'}\n"
            f"Цена: {contract['price']} ₽\n"
            f"Дата создания: {contract['created_at']}\n\n"
        )

        # Create a keyboard for more actions related to this contract (if needed)
        contract_detail_buttons = [
            [InlineKeyboardButton(text="Назад", callback_data="all_contracts")]
        ]

        await safe_edit_message(
            callback,
            text=contract_details,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=contract_detail_buttons)
        )
    else:
        await callback.answer("Контракт не найден.", show_alert=True)


# Главная функция
async def main() -> None:
    """Запуск бота."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем (KeyboardInterrupt).")
