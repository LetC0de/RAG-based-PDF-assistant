from flask import jsonify

def success_response(data=None, message=None):
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    return jsonify(response)

def error_response(code, message, status_code=400):
    return jsonify({
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }), status_code
