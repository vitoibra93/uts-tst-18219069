#IDENTITAS
#NAMA       : Muhammad Vito Ibrahim
#NIM        : 18219069
#DESKRIPSI  : File main.py API untuk operasi Authentication, Update, Delete, dan Add Menu.

#FROM & IMPORT STATEMENT
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

#Daftar Menu .json
import json
with open("menu.json", "r") as read_file:
    data = json.load(read_file)

#Objek Dibuat
app = FastAPI()

#AUTENTIKASI
# untuk mendapatkan string seperti di bawah ini run perintah di terminal:
# openssl rand -hex 32
SECRET_KEY = "fd317678802c480202cdfe85c0fd9243d9b254397bc9dd57c65342b64fb12b4a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "asdf": {
        "username": "asdf",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2y$10$rv6PAj0E7EurEBlo8dSRR.BSGbktzTO..SZGlSyaJVadw2.Sugp06",
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

#Mendefinisikan Fungsi Utilitas dan Akses Token
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

#Bagian Autentikasi
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

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