from docling.document_converter import DocumentConverter


def analyze(file_path: str):
    source = file_path  # PDF path or URL
    converter = DocumentConverter()
    result = converter.convert(source)
    return result.document.export_to_markdown()