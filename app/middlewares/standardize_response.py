from flask import jsonify

def standardize_response(response):
    # Convert the original response data from JSON string to Python dictionary
    original_data = response.get_json()

    # Construct the standardized response format
    standardized_data = {
        "status": 200,  
        "errors": {}, 
        "data": original_data  # The original data will be nested under the "data" key
    }

    # Set the response data to the standardized format
    response.set_data(jsonify(standardized_data))

    return response