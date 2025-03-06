from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class User(BaseModel):
    login: str
    password: str

class Message(BaseModel):
    username: str
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
    messages.append(msg.dict())
    return {"message": "Сообщение отправлено"}

@app.get("/messages")
def get_messages():
    return messages