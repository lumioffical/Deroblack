import json
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Загружаем пользователей из файла
try:
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)["users"]
except Exception as e:
    logger.error(f"Ошибка загрузки users.json: {e}")
    users = []

# Загружаем сообщения
try:
    with open("messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
except Exception as e:
    logger.warning(f"Ошибка загрузки messages.json: {e}. Создаём пустой файл.")
    messages = {}

    with open("messages.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

# Модель данных
class LoginData(BaseModel):
    login: str
    password: str

class MessageData(BaseModel):
    sender: str
    receiver: str
    text: str

@app.post("/login")
def login(data: LoginData):
    """Авторизация пользователя"""
    for user in users:
        if user["login"] == data.login and user["password"] == data.password:
            return {"status": "success"}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")

@app.get("/search")
def search_user(login: str):
    """Поиск пользователей по логину"""
    results = [user for user in users if login.lower() in user["login"].lower()]
    return results

@app.get("/messages/{user}")
def get_messages(user: str):
    """Получение сообщений пользователя"""
    return messages.get(user, [])

@app.post("/send")
def send_message(data: MessageData):
    """Отправка сообщения"""
    if not data.sender or not data.receiver or not data.text:
        raise HTTPException(status_code=400, detail="Некорректные данные")

    if data.receiver not in messages:
        messages[data.receiver] = []

    messages[data.receiver].append({"sender": data.sender, "text": data.text})

    # Сохраняем в файл
    try:
        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения messages.json: {e}")

    return {"status": "ok"}
