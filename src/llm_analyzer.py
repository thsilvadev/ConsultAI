

import ollama
import json

from pydantic import BaseModel
from sympy.physics.units import temperature


class Output(BaseModel):
    response: str

def process_exam(result_md, pacient_data):
    prompt_data = {
        "prompt": "Análise de exame médico",
        "md": result_md,
        "pacient_data": pacient_data
    }

    formatted_prompt = f"""
    1. Analise o exame anterior considerando os seguintes dados do paciente: `{pacient_data}`.
    2. Identifique pontos de atenção médica, valores anormais e riscos associados.
    3. Oriente o paciente sobre os próximos passos com base na análise.
    """

    system_prompt = f"""
     Você é um especialista em analisar exames médicos e clarear os pacientes sobre os resultados.
     
     Responda estritamente no seguinte formato JSON e em português do Brasil:
    ```json
    {{
        "response": "Texto explicativo sobre os achados médicos ao analisar o exame, evidenciando pontos de atenção e riscos e orientando o paciente."
    }}
    ```
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": str(result_md)},
        {"role": "user", "content": formatted_prompt}
    ]
    model ="mdubu/saaam_is_a_doctor"

    response = ollama.chat(model=model, messages=messages, stream=False, format=Output.model_json_schema(), options={temperature: 0.2})

    return response
