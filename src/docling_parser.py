from docling.document_converter import DocumentConverter
from docling.exceptions import ConversionError

def parse(file_path: str):
    try:
        source = file_path  # PDF path or URL
        converter = DocumentConverter()
        result = converter.convert(source, max_num_pages=15, max_file_size=20971520)
        return result.document.export_to_markdown()
    except ConversionError as e:
        # Capture specific errors related to docling conversion
        print(f"Erro ao converter o documento: {e}")
        return None  # Return None if conversion fails
    except Exception as e:
        # Capture any other exceptions that may occur
        print(f"Ocorreu um erro inesperado: {e}")
        return None  # Return None in case of unexpected errors