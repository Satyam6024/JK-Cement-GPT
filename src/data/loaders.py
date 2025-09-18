import pandas as pd
import json
import PyPDF2
from docx import Document
import xml.etree.ElementTree as ET
from typing import Any, Dict
from src.utils.db_connector import DatabaseConnector

class DataLoader:
    def __init__(self):
        self.db_connector = DatabaseConnector()
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, encoding='utf-8', low_memory=False)
    
    def load_excel(self, file_path: str) -> Dict[str, pd.DataFrame]:
        return pd.read_excel(file_path, sheet_name=None)
    
    def load_json(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_pdf(self, file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def load_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    def load_xml(self, file_path: str) -> Dict[str, Any]:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return self._xml_to_dict(root)
    
    def load_database(self, file_path: str, table_name: str = None) -> pd.DataFrame:
        if table_name:
            return self.db_connector.query_database(file_path, f"SELECT * FROM {table_name}")
        return self.db_connector.query_database(file_path)
    
    def _xml_to_dict(self, element) -> Dict[str, Any]:
        result = {}
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = self._xml_to_dict(child)
        return result