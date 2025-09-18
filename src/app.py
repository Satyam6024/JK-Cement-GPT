from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Enable CORS for frontend
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:5500'])
    
    # Serve the frontend
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Your existing API routes...
    app.register_blueprint(api_bp, url_prefix='/api')
    
    
    return app