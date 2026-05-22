from io import BytesIO

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream


class CVTextExtractor:
    def __init__(self, converter: DocumentConverter) -> None:
        self.converter = converter

    def _convert_to_doc_stream(self, cv: bytes) -> DocumentStream:
        Byte_IO = BytesIO(cv)
        return DocumentStream(name="doc", stream=Byte_IO)

    def extract_in_markdown(self, cv) -> str:
        source = self._convert_to_doc_stream(cv)
        return self.converter.convert(source=source).document.export_to_markdown()
