from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import json

app = FastAPI()

# Читаем пользователей из файла
def get_users():
    with open("users.json", "r") as file:
        return json.load(file)["users"]

class LoginRequest(BaseModel):
    login: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    users = get_users()
    for user in users:
        if user["login"] == request.login and user["password"] == request.password:
            return {"message": "Успешный вход"}
    raise HTTPException(status_code=401, detail="Неверные данные")