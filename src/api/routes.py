from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from src.pipelines.ingestion import DataIngestionPipeline
from src.pipelines.analysis import AnalysisPipeline
from src.models.rag_model import RAGModel
from src.config.config import Config

api_bp = Blueprint('api', __name__)
config = Config()
ingestion = DataIngestionPipeline()
analysis = AnalysisPipeline()
rag_model = RAGModel()

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        result = ingestion.process_file(file_path)
        return jsonify(result)

@api_bp.route('/query', methods=['POST'])
def query_data():
    data = request.get_json()
    query = data.get('query')
    analysis_type = data.get('analysis_type', 'general')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    result = analysis.perform_analysis(query, analysis_type)
    return jsonify(result)

@api_bp.route('/insights/<file_id>', methods=['GET'])
def get_insights(file_id):
    insights = rag_model.generate_insights(file_id)
    return jsonify(insights)

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    })

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    vector_stats = rag_model.vector_db.get_collection_stats()
    return jsonify({
        'documents_processed': vector_stats.get('document_count', 0),
        'supported_formats': config.SUPPORTED_FORMATS
    })