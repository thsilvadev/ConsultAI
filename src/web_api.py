from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile, Body, HTTPException
from docling_parser import parse
from datetime import datetime
import pytz
import json

from fastapi.middleware.cors import CORSMiddleware

# manaus time (só pra mostraTech)
manaus_tz = pytz.timezone('America/Manaus')
manaus_time = datetime.now(manaus_tz).strftime("%Y%m%d_%H%M%S")  # Formato válido para nomes de arquivo

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Substitua pelo domínio da sua aplicação
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os headers
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/document")
async def post_document(user_data: str = Body(...), file: UploadFile = File(...)):
    # Parse the string JSON into a Python dictionary
    # 1. Tenta parsear o JSON recebido
    try:
        user_data_dict = json.loads(user_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400,
                            detail="Erro ao processar user_data. Certifique-se de que seja um JSON válido.")

    nome = user_data_dict.get("nome", "").strip()
    if not nome:
        raise HTTPException(status_code=400, detail="Campo 'nome' está vazio ou ausente.")

    print("nome do paciente: ", nome)

    #trata o documento
    filename = file.filename
    file_content = await file.read()

    #armazenar o arquivo no disco
    file_path = f"./files/{manaus_time}_{nome}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    #manda pro docling
    result_md = parse(file_path)

    #manda pra LLM\

    #retorna pro client

    if result_md:
        return {"filename": filename, "message": result_md}
    else:
        raise HTTPException(
            status_code=400,
            detail="Arquivo não aceito. Favor enviar PDF ou DOCX de no máximo 15 páginas e de tamanho máximo 20MBs."
        )