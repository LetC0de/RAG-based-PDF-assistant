import os
from flask import Blueprint, request
from werkzeug.utils import secure_filename
from utils.response import success_response, error_response
from services.document_service import process_pdf
from services.vectorstore_service import clear_database, check_db_exists
from config import Config

document_bp = Blueprint('documents', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

@document_bp.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return error_response('INVALID_REQUEST', 'No file provided')

    file = request.files['file']

    if file.filename == '':
        return error_response('INVALID_REQUEST', 'No file selected')

    if not allowed_file(file.filename):
        return error_response('INVALID_FILE_TYPE', 'Only PDF files are allowed')

    try:
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

        filename = secure_filename(file.filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        result = process_pdf(file_path)

        os.remove(file_path)

        return success_response(
            data={
                "filename": filename,
                "chunks_created": result["chunks_created"],
                "processing_time": result["processing_time"]
            },
            message="Document processed successfully"
        )

    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return error_response('PROCESSING_ERROR', str(e), 500)

@document_bp.route('', methods=['DELETE'])
def delete_documents():
    if not check_db_exists():
        return error_response('VECTOR_DB_NOT_FOUND', 'No vector database found')

    try:
        clear_database()
        return success_response(message="Vector database cleared successfully")
    except Exception as e:
        return error_response('PROCESSING_ERROR', str(e), 500)
