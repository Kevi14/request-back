from app import app
from flask import jsonify

@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f"An error occurred: {error}")
    
    # Construct a custom error response
    response = jsonify({
        "status": 500,
        "errors": {"message": "An error occurred while processing the request."},
        "data": {}
    })
    response.status_code = 500
    return response