import os

from fastapi import FastAPI, File, UploadFile, Body, HTTPException
from starlette.requests import Request

from docling_parser import parse
from datetime import datetime
import pytz
import json
from fastapi.middleware.cors import CORSMiddleware
from llm_analyzer import process_exam
from groq_analyzer import groq_exam
import dotenv


dotenv.load_dotenv()

# manaus time (só pra mostraTech)
manaus_tz = pytz.timezone('America/Manaus')
manaus_time = datetime.now(manaus_tz).strftime("%Y%m%d_%H%M%S")  # Formato válido para nomes de arquivo

app = FastAPI()

# Middleware para adicionar headers CORS manualmente
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

# Configuração do CORS

origins = [
    "https://consult-ai-beta.vercel.app",
    "http://localhost:5173",
    "http://smoothly-apparent-hawk.ngrok-free.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Substitua pelo domínio da sua aplicação
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos os headers
)

@app.post("/document")
async def post_document(user_data: str = Body(...), file: UploadFile = File(...)):
    # Parse the string JSON into a Python dictionary
    # Tenta parsear o JSON recebido
    try:
        user_data_dict = json.loads(user_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400,
                            detail="Erro ao processar user_data. Certifique-se de que seja um JSON válido.")

    nome = user_data_dict.get("nome", "").strip()
    if not nome:
        raise HTTPException(status_code=400, detail="Campo 'nome' está vazio ou ausente.")

    print("dados do paciente: ", user_data_dict)

    #trata o documento
    filename = file.filename
    file_content = await file.read()

    #armazenar o arquivo no disco
    file_path = f"./files/{manaus_time}_{nome}"

    with open(file_path, "wb") as f:
        f.write(file_content)

    #manda pro docling
    result_md = parse(file_path)

    md_file_path = f"./md_files/{manaus_time}_{nome}.md"
    with open( md_file_path, "w", encoding="utf-8") as f:
        f.write(result_md)

    if result_md:
    #manda pra LLM\
        try:
            #output = process_exam(result_md, user_data_dict)
            output = groq_exam(result_md, user_data_dict, os.getenv("GROQ_API_KEY"))
            #retorna pro client
        except:
            raise HTTPException(
                status_code=400,
                detail="Problema durante interpretação da IA. Por favor, tente novamente mais tarde."
            )
        print(output)

        return {"output": output}
    else:
        raise HTTPException(
            status_code=400,
            detail="Arquivo não aceito. Favor enviar PDF ou DOCX de no máximo 15 páginas e de tamanho máximo 20MBs."
        )