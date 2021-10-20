#IDENTITAS
#NAMA       : Muhammad Vito Ibrahim
#NIM        : 18219069
#DESKRIPSI  : File main.py API untuk operasi Authentication, Update, Delete, dan Add Menu.

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

#Bagian MENU 1
import json
with open("menu.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

#AUTENTIKASI
# untuk mendapatkan string seperti di bawah ini run di terminal:
# openssl rand -hex 32
SECRET_KEY = "fd317678802c480202cdfe85c0fd9243d9b254397bc9dd57c65342b64fb12b4a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "asdf": {
        "username": "asdf",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Class Authentication
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str

#Function Authentication

#Bagian Menu 2
@app.get('/')
def root():
    return{'MENU':'NAMA MENU'}

#Membaca Menu
@app.get('/menu/{item_id}')
async def read_menu(item_id: int) :
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code= 404, detail=f'Item not found'
    )

#Menambah Menu
@app.post('/menu')
async def add_menu(name:str):
    id=1
    if(len(data["menu"])>0):
        id=data["menu"][len(data["menu"])-1]["id"]+1
    new_data={'id':id,'name':name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()
    return(new_data)
    raise HTTPException(
        status_code=500, detail=f'server error'
    )

#Menghapus Menu
@app.delete('/menu/{item_id}')
async def delete_menu(item_id:int):
    for menu_item in data['menu']:
        if menu_item['id']==item_id:
            data['menu'].remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()

            return{"message": "data berhasil dihapus"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

#Memperbarui Menu
@app.put('/menu/{item_id}')
async def update_menu(item_id: int, name:str):
    for menu_item in data['menu']:
        if menu_item['id']==item_id:
            menu_item['name']=name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()

            return{"message": "data berhasil diperbarui"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

