import pandas as pd
from typing import Dict, Any

class DataValidator:
    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        validation_report = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'stats': {}
        }
        
        if df.empty:
            validation_report['is_valid'] = False
            validation_report['issues'].append("DataFrame is empty")
            return validation_report
        
        for col in df.columns:
            null_count = df[col].isnull().sum()
            null_percentage = (null_count / len(df)) * 100
            
            if null_percentage > 50:
                validation_report['warnings'].append(f"Column '{col}' has {null_percentage:.1f}% missing values")
        
        if len(df.columns) != len(set(df.columns)):
            validation_report['issues'].append("Duplicate column names found")
        
        validation_report['stats'] = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'duplicate_rows': df.duplicated().sum()
        }
        
        return validation_report