from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Модели для клиентов
class ClientBase(BaseModel):
    name: str
    contact_info: Optional[str] = None

class ClientCreate(BaseModel):
    name: str
    contact_info: Optional[str] = None


class ContractCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: int


class ClientResponse(ClientBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Модели для контрактов
class ContractBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: int


class ContractCreate(ContractBase):
    pass


class ContractResponse(ContractBase):
    id: int
    client_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Модели для связей между клиентами и контрактами
class ClientContractLinkBase(BaseModel):
    client_id: int
    contract_id: int


class ClientContractLinkCreate(ClientContractLinkBase):
    pass


class ClientContractLinkResponse(ClientContractLinkBase):
    id: int
    linked_at: datetime

    class Config:
        orm_mode = True


# Дополнительные схемы для отображения связей
class ClientWithContractsResponse(ClientResponse):
    contracts: List[ContractResponse] = []


class ContractWithClientsResponse(ContractResponse):
    clients: List[ClientResponse] = []


class ClientWithContractsAndLinksResponse(ClientWithContractsResponse):
    client_contract_links: List[ClientContractLinkResponse] = []
