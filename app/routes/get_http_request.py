from app.models.request import HttpRequest
from app import app, db
from flask import request, jsonify, abort

@app.route('/api/HTTP/request/<int:request_id>/', methods=['GET'])
def get_http_request(request_id):
    try:
        # Fetch the HttpRequest object based on its ID from the database
        http_request = HttpRequest.query.get(request_id)

        # Check if the object exists
        if not http_request:
            raise ValueError(f"No HTTP request found for ID: {request_id}")

        # Return the data of the object
        return jsonify({
            "status": 200,
            "errors": {},
            "data": {
                "method": http_request.method,
                "request_data": http_request.request_data,
                "response_data": http_request.response_data,
                "status_code": http_request.status_code,
                "id": http_request.id
            }
        })

    except ValueError as e:
        # Handle custom validation errors or unsupported HTTP methods
        app.logger.error(f"ValueError occurred: {str(e)}")
        return jsonify({
            "status": 404,
            "errors": {"message": str(e)},
            "data": {}
        }), 404
    except Exception as e:
        # Handle other unexpected exceptions
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({
            "status": 500,
            "errors": {"message": "An unexpected error occurred."},
            "data": {}
        }), 500
