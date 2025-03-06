import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

app = FastAPI()

# Попытка загрузить users.json
try:
    with open("users.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or "users" not in data or not isinstance(data["users"], list):
        raise ValueError("Файл users.json должен содержать ключ 'users' со списком пользователей.")

    users = data["users"]
    logger.info("Файл users.json успешно загружен.")

except Exception as e:
    logger.error(f"Ошибка загрузки users.json: {e}")
    users = []

# Модель запроса для валидации входных данных
class LoginRequest(BaseModel):
    login: str
    password: str

# Функция проверки логина и пароля
def login_user(input_login: str, input_password: str) -> bool:
    for user in users:
        if isinstance(user, dict) and user.get("login") == input_login and user.get("password") == input_password:
            return True
    return False

@app.post("/login")
async def login(request: LoginRequest):
    logger.info(f"Попытка входа: login={request.login}, password={request.password}")

    if login_user(request.login, request.password):
        logger.info(f"Успешный вход: {request.login}")
        return {"message": "Success"}

    logger.warning(f"Неудачная попытка входа: {request.login}")
    raise HTTPException(status_code=401, detail="Unauthorized")
