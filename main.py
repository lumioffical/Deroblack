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
with open("users.json", "r") as file:
    users = json.load(file)

messages = []

@app.post("/login")
def login(user: User):
    for u in users:
        if u["login"] == user.login and u["password"] == user.password:
            return {"message": "Успешный вход"}
    raise HTTPException(status_code=401, detail="Неверный логин или пароль")

@app.post("/send")
def send_message(msg: Message):
    # Проверяем, есть ли отправитель и получатель среди пользователей
    if not any(u["login"] == msg.sender for u in users):
        raise HTTPException(status_code=404, detail="Отправитель не найден")
    if not any(u["login"] == msg.receiver for u in users):
        raise HTTPException(status_code=404, detail="Получатель не найден")

    messages.append(msg.dict())
    return {"message": "Сообщение отправлено"}

@app.get("/messages/{user}")
def get_messages(user: str):
    # Проверяем, существует ли такой пользователь
    if not any(u["login"] == user for u in users):
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Возвращаем только сообщения, где этот пользователь — получатель
    user_messages = [msg for msg in messages if msg["receiver"] == user]
    return user_messages