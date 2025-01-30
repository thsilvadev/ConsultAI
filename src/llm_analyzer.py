import ollama

# class Output(BaseModel):
#     response: str

def process_exam(result_md, pacient_data):
    prompt_data = {
        "prompt": "Análise de exame médico",
        "md": result_md,
        "pacient_data": pacient_data
    }

    formatted_prompt = f"""
    Responda-me no idioma português do Brasil (PT-BR):
    
    1. Analise o exame acima considerando os seguintes dados sobre mim: `{pacient_data}`.
    2. Identifique e aponte valores anormais e riscos associados.
    3. Oriente-me sobre os próximos passos com base na análise.
    """

    system_prompt = f"""
    **IMPORTANTE:** Responda APENAS em português do Brasil. Não use outros idiomas.
    
    * Você é um especialista em analisar exames médicos e instruir o paciente sobre os resultados.

    * Fale de forma clara e acessível, como um médico conversando com um paciente.

    ** Exemplo de resposta esperada:**  
    ```json
    {{
        "response": "Seu exame apresenta valores normais para glicose, mas há um pequeno aumento na pressão arterial. Recomendo manter uma dieta equilibrada e consultar um cardiologista."
    }}
    ```
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{str(result_md)} \n {formatted_prompt}"}
    ]
    models = ["llama3", "medllama2", "deepseek-r1", "mdubu/saaam_is_a_doctor"]

    response = ollama.chat(model=models[3], messages=messages, stream=False, options={"temperature": 0.3})

    return response
