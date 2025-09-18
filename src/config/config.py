import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')
    OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', './outputs')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './vector_db')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '104857600'))
    
    SUPPORTED_FORMATS = [
        'csv', 'xlsx', 'xls', 'json', 'pdf', 'docx', 
        'db', 'accdb', 'mdb', 'sqlite', 'sqlite3', 
        'fdb', 'dat', 'xml'
    ]