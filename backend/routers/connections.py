from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, schemas
from backend.database import get_db

router = APIRouter()

# Создание связи между клиентом и контрактом
@router.post("/client-contract-links")
async def create_client_contract_link(link: schemas.ClientContractLinkCreate, db: AsyncSession = Depends(get_db)):
    new_link = await crud.create_client_contract_link(db, link)
    return new_link

# Получение всех связей для клиента
@router.get("/clients/{client_id}/contracts")
async def get_client_contract_links(client_id: int, db: AsyncSession = Depends(get_db)):
    links = await crud.get_client_contract_links(db, client_id)
    return links

# Удаление связи между клиентом и контрактом
@router.delete("/client-contract-links/{client_id}/{contract_id}")
async def delete_client_contract_link(client_id: int, contract_id: int, db: AsyncSession = Depends(get_db)):
    link = await crud.delete_client_contract_link(db, client_id, contract_id)
    if not link:
        raise HTTPException(status_code=404, detail="Связь не найдена")
    return link  # Можно вернуть саму связь, если нужно, или просто сообщение об успехе
