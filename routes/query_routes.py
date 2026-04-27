from flask import Blueprint, request
from utils.response import success_response, error_response
from services.query_service import answer_question
from services.vectorstore_service import check_db_exists

query_bp = Blueprint('query', __name__)

@query_bp.route('', methods=['POST'])
def query_document():
    if not check_db_exists():
        return error_response('VECTOR_DB_NOT_FOUND', 'No vector database found. Please upload a PDF first.')

    data = request.get_json()

    if not data or 'question' not in data:
        return error_response('INVALID_REQUEST', 'Question is required')

    question = data['question'].strip()

    if not question:
        return error_response('INVALID_REQUEST', 'Question cannot be empty')

    try:
        result = answer_question(question)

        if result is None:
            return error_response('VECTOR_DB_NOT_FOUND', 'No vector database found. Please upload a PDF first.')

        return success_response(data=result)

    except Exception as e:
        return error_response('MISTRAL_API_ERROR', str(e), 500)
