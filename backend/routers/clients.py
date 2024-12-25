from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import ClientCreate, ClientResponse
from backend.crud import create_or_update_client, delete_client, get_client_by_name, get_clients

router = APIRouter()

@router.post("/")
async def create_new_client(client: ClientCreate, db: AsyncSession = Depends(get_db)):
    """Создать нового клиента."""
    created_client = await create_or_update_client(db, client.name, client.contact_info)
    if not created_client:
        raise HTTPException(status_code=400, detail="Ошибка при создании клиента")
    return created_client.as_dict()  # Возвращаем данные клиента как словарь


@router.delete("/{client_id}")
async def delete_existing_client(client_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить клиента по ID."""
    deleted_client = await delete_client(db, client_id)
    if not deleted_client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return deleted_client.as_dict()  # Возвращаем удаленного клиента как словарь


@router.get("/")
async def get_all_clients(db: AsyncSession = Depends(get_db)):
    """Получить всех клиентов."""
    clients = await get_clients(db)
    return [client for client in clients]  # Возвращаем список клиентов в виде словарей


@router.get("/{client_name}")
async def get_client_by_name_route(client_name: str, db: AsyncSession = Depends(get_db)):
    """Получить клиента по имени."""
    client = await get_client_by_name(db, client_name)
    if not client:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return client.as_dict()  # Возвращаем клиента как словарь
