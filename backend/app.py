from flask import Flask
from flask_cors import CORS
from routes.document_routes import document_bp
from routes.query_routes import query_bp
from services.vectorstore_service import check_db_exists
from utils.response import success_response
from config import Config

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE

app.register_blueprint(document_bp, url_prefix='/api/documents')
app.register_blueprint(query_bp, url_prefix='/api/query')

@app.route('/api/health', methods=['GET'])
def health_check():
    return success_response(data={
        "status": "healthy",
        "vector_db_exists": check_db_exists(),
        "mistral_api_configured": Config.MISTRAL_API_KEY is not None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
