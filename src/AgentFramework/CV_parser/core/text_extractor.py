from io import BytesIO
import logging

from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from utils.exception import TextExtractionError

logger = logging.getLogger(__name__)

class CVTextExtractor:
    def __init__(self, converter: DocumentConverter) -> None:
        self.converter = converter

    def _convert_to_doc_stream(self, cv: bytes) -> DocumentStream:
        byte_io = BytesIO(cv)
        return DocumentStream(name="doc", stream=byte_io)

    def extract_in_markdown(self, cv: bytes) -> str:
        source = self._convert_to_doc_stream(cv)
        try:
            logger.info("Extracting Text from CV")
            result = self.converter.convert(source=source).document.export_to_markdown()
        except Exception as e:
            logger.exception("Text Extraction failed")
            raise TextExtractionError("Text extraction from CV document failed") from e
        logger.info("Text extraction complete")
        return result