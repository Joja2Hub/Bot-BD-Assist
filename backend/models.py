from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base  # Базовый класс для моделей


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    contracts = relationship("Contract", back_populates="client")
    client_contract_links = relationship("ClientContractLink", back_populates="client")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact_info": self.contact_info,
            "created_at": self.created_at
        }

class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    client = relationship("Client", back_populates="contracts")  # Обратная связь с Client
    client_contract_links = relationship("ClientContractLink", back_populates="contract")

    def as_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "created_at": self.created_at
        }

class ClientContractLink(Base):
    __tablename__ = "client_contract_links"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    linked_at = Column(DateTime, server_default=func.now())

    client = relationship("Client", back_populates="client_contract_links")  # Обратная связь с Client
    contract = relationship("Contract", back_populates="client_contract_links")  # Обратная связь с Contract

    __table_args__ = (UniqueConstraint('client_id', 'contract_id', name='_client_contract_uc'),)

    def as_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "contract_id": self.contract_id,
            "linked_at": self.linked_at
        }
