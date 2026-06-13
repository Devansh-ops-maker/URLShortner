from database import cnx
from fastapi import FastAPI,Request
import os
from dotenv import load_dotenv
import sqlite3
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

conn=sqlite3.connect(os.getenv("DB_DATABASE"))

def Converter(id): # Converts a normal to url to unique base 62 encoded value
    val=""
    temp=id
    if(temp==0):
         return "0"
    while(temp>0):
        rem=temp%62
        if(rem<=9):
            val=str(rem)+val
        else:
            rem-=10
            if(rem<26):
                val=(chr(ord('a')+rem))+val
            else:
                rem-=26
                val=(chr(ord('A')+rem))+val
        temp=temp//62
    return val
def Convert_back(uuid):
    val = 0
    uuid=uuid[1:-1]

    for ch in uuid:
        if '0' <= ch <= '9':
            digit = ord(ch) - ord('0')
        elif 'a' <= ch <= 'z':
            digit = ord(ch) - ord('a') + 10
        elif 'A' <= ch <= 'Z':
            digit = ord(ch) - ord('A') + 36
        else:
            raise ValueError("Invalid Base62 character")

        val = val * 62 + digit

    return val

app=FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html"
)
@app.get("/url/")
async def work(url:str):
    cursor=cnx.cursor()
    query="SELECT id FROM URLS WHERE url=%s"
    cursor.execute(query,(url,))
    result=cursor.fetchone()
    if result is None:
        query2="INSERT INTO URLS (url) VALUES (%s)"
        cursor.execute(query2,(url,))
        cnx.commit()
    cursor.execute(query,(url,))
    result=cursor.fetchone()
    uuid=Converter(result[0])
    return uuid
@app.get("/shorten")
async def short(uuid:str):
    id=Convert_back(uuid)
    print(id)
    print(uuid)
    query="SELECT URL FROM URLS WHERE id=%s"
    cursor=cnx.cursor()
    cursor.execute(query,(id,))
    url=cursor.fetchone()
    if url is None:
        return {"error":"URL Not Found"}
    else:
        return RedirectResponse(url[0])



    
    