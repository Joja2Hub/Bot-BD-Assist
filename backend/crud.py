from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from backend import models
from backend.models import Client, Contract, ClientContractLink
from backend.schemas import ClientCreate, ContractCreate, ClientContractLinkCreate


# CRUD для клиентов
async def create_or_update_client(db: AsyncSession, name: str, contact_info: str = None):
    """Создать или обновить клиента."""
    result = await db.execute(select(Client).filter(Client.name == name))
    client = result.scalar_one_or_none()

    if client is None:
        client = Client(name=name, contact_info=contact_info)
        db.add(client)
    else:
        if client.contact_info != contact_info:
            client.contact_info = contact_info

    try:
        await db.commit()
        await db.refresh(client)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении клиента: {str(e)}")

    return client


async def get_clients(db: AsyncSession):
    """Получить всех клиентов."""
    result = await db.execute(select(Client))
    return result.scalars().all()


async def get_client_by_name(db: AsyncSession, name: str):
    """Получить клиента по имени."""
    result = await db.execute(select(Client).filter(Client.name == name))
    return result.scalar_one_or_none()


# CRUD для контрактов
async def create_contract(db: AsyncSession, contract: ContractCreate):
    """Создать новый контракт."""
    new_contract = Contract(**contract.dict())
    db.add(new_contract)

    try:
        await db.commit()
        await db.refresh(new_contract)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании контракта: {str(e)}")

    return new_contract


async def get_contracts(db: AsyncSession):
    """Получить все контракты."""
    result = await db.execute(select(Contract))
    return result.scalars().all()


async def get_contract_by_id(db: AsyncSession, contract_id: int):
    """Получить контракт по ID."""
    result = await db.execute(select(Contract).filter(Contract.id == contract_id))
    return result.scalar_one_or_none()


# CRUD для связей клиента с контрактами
async def create_client_contract_link(db: AsyncSession, link: ClientContractLinkCreate):
    """Создать связь клиента и контракта."""
    # Проверяем, существует ли уже эта связь
    existing_link = await db.execute(
        select(ClientContractLink).filter(
            ClientContractLink.client_id == link.client_id,
            ClientContractLink.contract_id == link.contract_id
        )
    )
    if existing_link.scalars().first():
        raise HTTPException(status_code=400, detail="Связь уже существует")

    # Создаем новую связь
    new_link = ClientContractLink(client_id=link.client_id, contract_id=link.contract_id)
    db.add(new_link)

    try:
        await db.commit()
        await db.refresh(new_link)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании связи: {str(e)}")

    return new_link


async def get_client_contract_links(db: AsyncSession):
    """Получить все связи клиентов с контрактами."""
    result = await db.execute(select(ClientContractLink))
    return result.scalars().all()


async def get_client_contract_link_by_client_and_contract(db: AsyncSession, client_id: int, contract_id: int):
    """Получить связь между клиентом и контрактом."""
    result = await db.execute(
        select(ClientContractLink).filter(
            ClientContractLink.client_id == client_id,
            ClientContractLink.contract_id == contract_id
        )
    )
    return result.scalar_one_or_none()


# Создание нового клиента
async def create_client(db: AsyncSession, client: ClientCreate):
    """Создать нового клиента."""
    new_client = Client(**client.dict())
    db.add(new_client)

    try:
        await db.commit()
        await db.refresh(new_client)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании клиента: {str(e)}")

    return new_client


# Удаление клиента по ID
async def delete_client(db: AsyncSession, client_id: int):
    """Удалить клиента по ID."""
    result = await db.execute(select(Client).filter(Client.id == client_id))
    client = result.scalars().first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        await db.delete(client)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении клиента: {str(e)}")

    return client

# Создание нового контракта
async def create_contract(db: AsyncSession, contract: ContractCreate, client_id: int):
    """Создать новый контракт для клиента."""
    new_contract = Contract(**contract.dict(), client_id=client_id)
    db.add(new_contract)

    try:
        await db.commit()
        await db.refresh(new_contract)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании контракта: {str(e)}")

    return new_contract


# Удаление контракта по ID
async def delete_contract(db: AsyncSession, contract_id: int):
    """Удалить контракт по ID."""
    result = await db.execute(select(Contract).filter(Contract.id == contract_id))
    contract = result.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    try:
        await db.delete(contract)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении контракта: {str(e)}")

    return contract


# Создание связи между клиентом и контрактом
async def create_client_contract_link(db: AsyncSession, link: ClientContractLinkCreate):
    # Проверяем, существует ли клиент и контракт
    client = await db.execute(select(Client).filter(Client.id == link.client_id))
    client = client.scalars().first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    contract = await db.execute(select(Contract).filter(Contract.id == link.contract_id))
    contract = contract.scalars().first()

    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    # Создаем связь
    new_link = ClientContractLink(client_id=link.client_id, contract_id=link.contract_id)
    db.add(new_link)
    try:
        await db.commit()
        await db.refresh(new_link)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating link: {str(e)}")

    return new_link


# Получение всех связей для клиента
async def get_client_contract_links(db: AsyncSession, client_id: int):
    result = await db.execute(select(ClientContractLink).filter(ClientContractLink.client_id == client_id))
    return result.scalars().all()


# Удаление связи между клиентом и контрактом
async def delete_client_contract_link(db: AsyncSession, client_id: int, contract_id: int):
    result = await db.execute(select(ClientContractLink).filter(ClientContractLink.client_id == client_id,
                                                                ClientContractLink.contract_id == contract_id))
    link = result.scalars().first()

    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    try:
        await db.delete(link)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting link: {str(e)}")

    return link


async def check_client_contract_links(db: AsyncSession, client_id: int) -> bool:
    """Проверяет, есть ли связи клиента с контрактами."""
    result = await db.execute(select(ClientContractLink).filter(ClientContractLink.client_id == client_id))
    links = result.scalars().all()
    return len(links) > 0  # Возвращаем True, если есть хотя бы одна связь
