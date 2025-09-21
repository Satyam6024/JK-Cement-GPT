from flask import Flask, render_template
from flask_cors import CORS
import os
from src.config.config import Config
from src.api.routes import api_bp

def create_app():
    # Set template folder relative to src directory
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(Config)
    
    CORS(app, origins=['*'])
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create directories
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)