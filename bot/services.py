import logging
import aiohttp
from config import BACKEND_URL

# Инициализация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Универсальная функция для отправки GET-запросов
async def fetch_data(endpoint: str):
    """Получение данных с бэкенда."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/{endpoint}") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Успешно получены данные с бэкенда: {len(data)} записей.")
                    return data
                else:
                    logger.error(f"Ошибка при получении данных с бэкенда: {response.status}")
                    return []
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду: {e}")
        return []


# Универсальная функция для отправки POST-запросов
async def post_data(endpoint: str, data: dict):
    """Отправка данных на бэкенд."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BACKEND_URL}/{endpoint}", json=data) as response:
                logger.info(f"Ответ от сервера: {response.status} для запроса {endpoint} с данными {data}")
                if response.status == 200 or response.status == 201:
                    response_data = await response.json()
                    logger.info(f"Успешно отправлены данные на бэкенд: {response.status}, {response_data}")
                    response_data["status"] = "success"
                    return response_data
                else:
                    logger.error(f"Ошибка при отправке данных на бэкенд: {response.status}, {await response.text()}")
                    return {"status": "error"}

    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду: {e}")
        return {}


# Универсальная функция для отправки DELETE-запросов
async def delete_data(endpoint: str):
    """Отправка DELETE-запроса на бэкенд."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{BACKEND_URL}/{endpoint}") as response:
                if response.status == 200:
                    response_data = await response.json()
                    response_data["status"] = "success"
                    return response_data
                else:
                    logger.error(f"Ошибка при удалении данных на бэкенде: {response.status}")
                    return {"status": "error"}
    except aiohttp.ClientError as e:
        logger.error(f"Ошибка при подключении к бэкенду для удаления данных: {e}")
        return {}


# Получение всех контрактов
async def fetch_all_contracts():
    """Получение всех контрактов с бэкенда."""
    return await fetch_data("contracts/")

# Получение контракта по ID
async def get_contract_by_id(contract_id: int):
    """Получение информации о контракте по ID."""
    return await fetch_data(f"contracts/{contract_id}")

# Добавление нового контракта
async def add_contract(contract_data: dict):
    """Добавление контракта через бэкенд."""
    return await post_data("contracts/", contract_data)

# Удаление контракта по ID
async def remove_contract(contract_id: int):
    """Удаление контракта через бэкенд."""
    return await delete_data(f"contracts/{contract_id}")

# Получение списка клиентов
async def fetch_clients():
    """Получение списка клиентов с бэкенда."""
    return await fetch_data("clients/")

# Получение клиента по ID
async def get_client_by_id(client_id: int):
    """Получение информации о клиенте по ID."""
    return await fetch_data(f"clients/{client_id}")

# Добавление нового клиента
async def add_client(client_data: dict):
    """Добавление клиента через бэкенд."""
    return await post_data("clients/", client_data)

# Удаление клиента по ID
async def remove_client(client_id: int):
    """Удаление клиента через бэкенд."""
    return await delete_data(f"clients/{client_id}")


async def fetch_client_contract_links_from_backend(client_id: int):
    """Получаем все связи между клиентом и контрактами с бэкенда."""
    return await fetch_data(f"client-contract-links/{client_id}")


