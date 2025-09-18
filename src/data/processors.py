import pandas as pd
import numpy as np
from typing import Dict, List, Any

class DataProcessor:
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        
        for col in df_clean.columns:
            if df_clean[col].dtype in ['object', 'string']:
                df_clean[col].fillna('Unknown', inplace=True)
            else:
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
        
        df_clean.drop_duplicates(inplace=True)
        return df_clean
    
    def generate_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        summary = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_summary': df.describe().to_dict() if not df.select_dtypes(include=[np.number]).empty else {},
            'categorical_summary': {col: df[col].value_counts().head().to_dict() 
                                  for col in df.select_dtypes(include=['object']).columns}
        }
        return summary
    
    def chunk_data(self, data: Any, chunk_size: int = 1000) -> List[str]:
        if isinstance(data, pd.DataFrame):
            chunks = []
            for i in range(0, len(data), chunk_size):
                chunk = data.iloc[i:i+chunk_size]
                chunks.append(chunk.to_string())
            return chunks
        elif isinstance(data, str):
            return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        return [str(data)]