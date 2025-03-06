import json
import logging
from fastapi import FastAPI, HTTPException

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Загружаем пользователей из файла
try:
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
        if not isinstance(users, list):
            raise ValueError("Файл users.json должен содержать список пользователей.")
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    logger.error(f"Ошибка загрузки users.json: {e}")
    users = []

# Загружаем сообщения
try:
    with open("messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
        if not isinstance(messages, dict):
            raise ValueError("Файл messages.json должен содержать словарь сообщений.")
except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
    logger.warning(f"Ошибка загрузки messages.json: {e}. Создаём пустой.")
    messages = {}

@app.get("/search")
def search_user(name: str):
    """Поиск пользователей по имени"""
    if not name:
        raise HTTPException(status_code=400, detail="Имя не должно быть пустым")
    
    results = [user for user in users if "name" in user and name.lower() in user["name"].lower()]
    return results

@app.get("/messages")
def get_messages(user: int):
    """Получение сообщений пользователя"""
    return messages.get(str(user), [])

@app.post("/send")
def send_message(data: dict):
    """Отправка сообщения"""
    user_id = str(data.get("to"))
    text = data.get("text")

    if not user_id or not text:
        raise HTTPException(status_code=400, detail="Некорректные данные")

    if user_id not in messages:
        messages[user_id] = []

    messages[user_id].append({"text": text, "sender": "them"})

    # Сохраняем в файл
    try:
        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения messages.json: {e}")

    return {"status": "ok"}
