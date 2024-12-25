from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import ContractCreate, ContractResponse
from backend.crud import create_contract, delete_contract, get_contract_by_id, get_contracts

router = APIRouter()

@router.post("/")
async def create_new_contract(contract: ContractCreate, client_id: int, db: AsyncSession = Depends(get_db)):
    """Создать новый контракт для клиента."""
    created_contract = await create_contract(db, contract, client_id)
    if not created_contract:
        raise HTTPException(status_code=400, detail="Ошибка при создании контракта")
    return created_contract.as_dict()  # Возвращаем данные контракта как словарь


@router.delete("/{contract_id}")
async def delete_existing_contract(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Удалить контракт по ID."""
    deleted_contract = await delete_contract(db, contract_id)
    if not deleted_contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    return deleted_contract  # Возвращаем удаленный контракт как словарь


@router.get("/")
async def get_all_contracts(db: AsyncSession = Depends(get_db)):
    """Получить все контракты."""
    contracts = await get_contracts(db)
    return [contract for contract in contracts]  # Возвращаем список контрактов как словари


@router.get("/{contract_id}")
async def get_contract_by_id_route(contract_id: int, db: AsyncSession = Depends(get_db)):
    """Получить контракт по ID."""
    contract = await get_contract_by_id(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Контракт не найден")
    return contract  # Возвращаем контракт как словарь
