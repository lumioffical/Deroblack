from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class User(BaseModel):
    login: str
    password: str

class Message(BaseModel):
    sender: str
    receiver: str
    message: str

# Загружаем пользователей
with open("users.json", "r", encoding="utf-8") as file:
    users = json.load(file)["users"]

# Проверяем, что данные в users корректные
if not isinstance(users, list) or not all(isinstance(u, dict) for u in users):
    raise ValueError("Файл users.json должен содержать список словарей.")

messages = []

@app.post("/login")
def login(user: User):
    for u in users:
        if isinstance(u, dict) and u.get("login") == user.login and u.get("password") == user.password:
            return {"message": "Успешный вход"}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")

@app.post("/send")
def send_message(msg: Message):
    if not any(u.get("login") == msg.sender for u in users):
        raise HTTPException(status_code=404, detail="Отправитель не найден")
    if not any(u.get("login") == msg.receiver for u in users):
        raise HTTPException(status_code=404, detail="Получатель не найден")

    messages.append(msg.dict())
    return {"message": "Сообщение отправлено"}

@app.get("/messages/{user}")
def get_messages(user: str):
    if not any(u.get("login") == user for u in users):
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return [msg for msg in messages if msg["receiver"] == user]
