from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Body
from docling_parser import analyze
from datetime import datetime
import pytz
import json

# manaus time (só pra mostraTech)
manaus_tz = pytz.timezone('America/Manaus')
manaus_time = datetime.now(manaus_tz).strftime("%Y%m%d_%H%M%S")  # Formato válido para nomes de arquivo

app = FastAPI()

# classes de objetos
class UserData(BaseModel):
    nome: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/document")
async def post_document(user_data: str = Body(...), file: UploadFile = File(...)):
    # Parse the string JSON into a Python dictionary
    user_data_dict = json.loads(user_data)
    nome = user_data_dict.get("nome", "default_name")  # Access the 'nome' key

    print("nome do paciente: ", nome)

    #trata o documento
    filename = file.filename
    file_content = await file.read()

    #armazenar o arquivo no disco
    file_path = f"./files/{manaus_time}_{nome}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    #manda pro docling
    result_md = analyze(file_path)

    #manda pra LLM

    print(result_md)

    return {"filename": filename, "message": result_md}
