import os
from pathlib import Path
from typing import Dict, Any
from src.config.config import Config

class FileHandler:
    def __init__(self):
        self.config = Config()
    
    def validate_file(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        ext = Path(file_path).suffix[1:].lower()
        return ext in self.config.SUPPORTED_FORMATS
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'size': stat.st_size,
            'extension': Path(file_path).suffix[1:].lower(),
            'modified': stat.st_mtime
        }
    
    def safe_filename(self, filename: str) -> str:
        return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()