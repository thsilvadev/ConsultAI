import json
import ollama


def extract_exams_from_text(text, reference_exams):
    """
    Usa a LLM para extrair exames do texto e compará-los com os exames de referência,
    retornando um JSON com os exames encontrados no arquivo .md.
    """
    prompt = (
            """
            Você receberá um texto contendo um laudo de exame e uma lista de exames de referência.
            Sua tarefa é extrair apenas os exames que aparecem no laudo e retornar uma lista no formato JSON.
    
            Formato esperado:
            [
                {"exam": "Nome do Exame", "subExam": "Subexame", "value": "Valor"},
                {"exam": "Nome do Exame", "subExam": "Subexame", "value": "Valor"}
            ]
    
            Caso um exame do laudo não esteja na lista de referência, ignore-o.
            Aqui está a lista de exames de referência:
            """ + json.dumps(reference_exams, ensure_ascii=False, indent=2) + """

        Agora, analise este laudo e extraia os exames correspondentes:
        """ + text + ""
    )

    response = ollama.chat(model='deepseek-r1', messages=[{"role": "user", "content": prompt}])

    try:
        extracted_data = json.loads(response["message"]["content"])
        return extracted_data
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta da LLM.")
        return []

def main():
    # Carregar o conteúdo dos arquivos
    with open("./md_files/20250130_145131_Maria da Gloria.md", "r", encoding="utf-8") as md_file:
        exam_text = md_file.read()

    with open("./assets/exames_referencia.txt", "r", encoding="utf-8") as ref_file:
        reference_exams = ref_file.read()

    # Extrair exames do texto
    extracted_exams = extract_exams_from_text(exam_text, reference_exams)

    # Salvar a saída em um arquivo JSON
    with open("resultado_exames.json", "w", encoding="utf-8") as output_file:
        json.dump(extracted_exams, output_file, ensure_ascii=False, indent=2)

    print("Extração concluída! Resultados salvos em resultado_exames.json")

if __name__ == "__main__":
    main()