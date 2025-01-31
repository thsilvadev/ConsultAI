import os
from groq import Groq




def groq_exam(result_md, pacient_data, api_key):

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
     
     "Seu exame apresenta valores normais para glicose, mas há um pequeno aumento na pressão arterial. Recomendo manter uma dieta equilibrada e consultar um cardiologista."
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{str(result_md)} \n {formatted_prompt}"}
    ]
    models = ["llama3", "medllama2", "deepseek-r1", "mdubu/saaam_is_a_doctor",  "llama3-8b-8192"]

    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=models[4],
    )
    return chat_completion.choices[0].message.content
