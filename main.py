#IDENTITAS
#NAMA       : Muhammad Vito Ibrahim
#NIM        : 18219069
#DESKRIPSI  : File main.py API untuk operasi Authentication, Update, Delete, dan Add Menu.

import json
from fastapi import FastAPI, HTTPException
with open("menu.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

#AUTENTIKASI


#Bagian MENU
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

