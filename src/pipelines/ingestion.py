import os
import uuid
import pandas as pd
from typing import Dict, Any
from src.data.loaders import DataLoader
from src.data.processors import DataProcessor
from src.data.validators import DataValidator
from src.models.rag_model import RAGModel

class DataIngestionPipeline:
    def __init__(self):
        self.loader = DataLoader()
        self.processor = DataProcessor()
        self.validator = DataValidator()
        self.rag_model = RAGModel()
        
    def process_file(self, file_path: str) -> Dict[str, Any]:
        file_id = str(uuid.uuid4())
        ext = os.path.splitext(file_path)[1][1:].lower()
        
        try:
            if ext == 'csv':
                data = self.loader.load_csv(file_path)
                processed_data = self.processor.clean_data(data)
                validation = self.validator.validate_dataframe(processed_data)
                
            elif ext in ['xlsx', 'xls']:
                data_sheets = self.loader.load_excel(file_path)
                processed_data = {}
                validation = {'sheets': {}}
                for sheet, df in data_sheets.items():
                    processed_data[sheet] = self.processor.clean_data(df)
                    validation['sheets'][sheet] = self.validator.validate_dataframe(df)
                
            elif ext == 'json':
                data = self.loader.load_json(file_path)
                processed_data = data
                validation = {'is_valid': True, 'type': 'json'}
                
            elif ext == 'pdf':
                data = self.loader.load_pdf(file_path)
                processed_data = data
                validation = {'is_valid': True, 'type': 'pdf'}
                
            elif ext in ['db', 'sqlite', 'sqlite3', 'accdb', 'mdb']:
                data = self.loader.load_database(file_path)
                processed_data = self.processor.clean_data(data)
                validation = self.validator.validate_dataframe(processed_data)
                
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            metadata = {
                'file_id': file_id,
                'filename': os.path.basename(file_path),
                'file_type': ext,
                'processed_at': pd.Timestamp.now().isoformat()
            }
            
            self.rag_model.ingest_data(processed_data, metadata)
            
            return {
                'file_id': file_id,
                'status': 'success',
                'validation': validation,
                'metadata': metadata,
                'summary': self.processor.generate_summary(processed_data) if hasattr(processed_data, 'describe') else None
            }
            
        except Exception as e:
            return {
                'file_id': file_id,
                'status': 'error',
                'error': str(e)
            }