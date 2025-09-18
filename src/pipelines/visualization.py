import plotly.express as px
import pandas as pd
from typing import Dict, Any

class VisualizationPipeline:
    def __init__(self):
        self.chart_types = ['bar', 'line', 'scatter', 'histogram', 'heatmap']
    
    def generate_visualization(self, data: pd.DataFrame, chart_type: str, **kwargs) -> Dict[str, Any]:
        try:
            if chart_type == 'bar':
                return self._create_bar_chart(data, **kwargs)
            elif chart_type == 'line':
                return self._create_line_chart(data, **kwargs)
            elif chart_type == 'scatter':
                return self._create_scatter_plot(data, **kwargs)
            elif chart_type == 'histogram':
                return self._create_histogram(data, **kwargs)
            elif chart_type == 'heatmap':
                return self._create_heatmap(data, **kwargs)
            else:
                return self._create_auto_chart(data)
        except Exception as e:
            return {'error': str(e), 'chart_html': None}
    
    def _create_bar_chart(self, data: pd.DataFrame, x_col: str = None, y_col: str = None) -> Dict[str, Any]:
        if not x_col:
            x_col = data.columns[0]
        if not y_col:
            y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0]
        
        fig = px.bar(data, x=x_col, y=y_col, title=f'{y_col} by {x_col}')
        return {
            'chart_html': fig.to_html(),
            'chart_type': 'bar',
            'description': f'Bar chart showing {y_col} across different {x_col} values'
        }
    
    def _create_line_chart(self, data: pd.DataFrame, x_col: str = None, y_col: str = None) -> Dict[str, Any]:
        if not x_col:
            x_col = data.columns[0]
        if not y_col:
            y_col = data.columns[1] if len(data.columns) > 1 else data.columns[0]
        
        fig = px.line(data, x=x_col, y=y_col, title=f'{y_col} Trend over {x_col}')
        return {
            'chart_html': fig.to_html(),
            'chart_type': 'line',
            'description': f'Line chart showing trend of {y_col} over {x_col}'
        }
    
    def _create_scatter_plot(self, data: pd.DataFrame, x_col: str = None, y_col: str = None) -> Dict[str, Any]:
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) < 2:
            return {'error': 'Need at least 2 numeric columns for scatter plot'}
        
        x_col = x_col or numeric_cols[0]
        y_col = y_col or numeric_cols[1]
        
        fig = px.scatter(data, x=x_col, y=y_col, title=f'{y_col} vs {x_col}')
        return {
            'chart_html': fig.to_html(),
            'chart_type': 'scatter'
        }
    
    def _create_histogram(self, data: pd.DataFrame, col: str = None) -> Dict[str, Any]:
        numeric_cols = data.select_dtypes(include=['number']).columns
        if numeric_cols.empty:
            return {'error': 'No numeric columns found for histogram'}
        
        col = col or numeric_cols[0]
        fig = px.histogram(data, x=col, title=f'Distribution of {col}')
        return {
            'chart_html': fig.to_html(),
            'chart_type': 'histogram'
        }
    
    def _create_heatmap(self, data: pd.DataFrame) -> Dict[str, Any]:
        numeric_data = data.select_dtypes(include=['number'])
        if numeric_data.empty:
            return {'error': 'No numeric data for correlation heatmap'}
        
        corr_matrix = numeric_data.corr()
        fig = px.imshow(corr_matrix, text_auto=True, title='Correlation Heatmap')
        return {
            'chart_html': fig.to_html(),
            'chart_type': 'heatmap'
        }
    
    def _create_auto_chart(self, data: pd.DataFrame) -> Dict[str, Any]:
        numeric_cols = data.select_dtypes(include=['number']).columns
        categorical_cols = data.select_dtypes(include=['object']).columns
        
        if len(numeric_cols) >= 2:
            return self._create_scatter_plot(data)
        elif len(numeric_cols) == 1 and len(categorical_cols) >= 1:
            return self._create_bar_chart(data, categorical_cols[0], numeric_cols[0])
        elif len(numeric_cols) == 1:
            return self._create_histogram(data, numeric_cols[0])
        else:
            return {'error': 'Unable to determine appropriate chart type'}
