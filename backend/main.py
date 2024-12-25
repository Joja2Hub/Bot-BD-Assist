from fastapi import FastAPI
from backend.routers import clients, contracts, connections  # Подключаем роутеры

# Создаем приложение FastAPI
app = FastAPI()

# Регистрируем роутеры с уникальными префиксами
app.include_router(clients.router, prefix="/clients", tags=["Clients"])
app.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
app.include_router(connections.router, prefix="/links", tags=["Client-Contract Links"])

# Тестовый эндпоинт
@app.get("/")
async def root():
    return {"message": "API для управления клиентами и контрактами запущено!"}
