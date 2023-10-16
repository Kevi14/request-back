from flask import request, jsonify, abort
from app import app, db
import requests
from app.models.request import HttpRequest
from urllib.parse import urlparse

@app.route('/api/HTTP/<string:method>/', methods=['GET', 'POST'])
def http_request(method):
    try:
        # Get the URL from the query parameters
        url = request.args.get('url')

        # Validate the URL
        if not url:
            raise ValueError("URL is missing in the request")

        # Dictionary to map HTTP methods to their respective functions in `requests`
        METHODS = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete,
        }

        # Check if the method is valid
        if method.upper() not in METHODS:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Use the mapped function from the dictionary
        response = METHODS[method.upper()](url, allow_redirects=True)
        # Check for a successful response, else raise an exception
        # response.raise_for_status()

        # Tracking redirects
        redirects = []
        for r in response.history:
            # Extract the domain and path of the redirect URL
            parsed_r_url = urlparse(r.url)
            parsed_original_url = urlparse(url)

            # Check if the domains match
            if parsed_r_url.netloc == parsed_original_url.netloc:
                location_value = parsed_r_url.path
            else:
                location_value = r.url

            redirect_data = {
                "url": location_value,
                "status_code": r.status_code,
                "headers": dict(r.headers)
            }
            # Update the 'Location' in headers, if exists
            if "Location" in redirect_data["headers"]:
                redirect_data["headers"]["Location"] = location_value

            redirects.append(redirect_data)
        # Create final response data
        responses_list = redirects + [{
            "url": response.url,
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }]

        # Save to the database
        http_request = HttpRequest(
            method=method,
            request_data={
                "url": url,  # Save the request URL here
                "headers": dict(request.headers),
                "body": request.data.decode()  # Decoding the body to a string
            },
            response_data=responses_list,
            status_code=response.status_code
        )
        db.session.add(http_request)
        db.session.commit()

        # Return the result
        return jsonify({
            "status": 200,
            "errors": {},
            "data": {
                "response": responses_list,
                "request": {
                    "headers": dict(request.headers),
                    "body": request.data.decode(),
                    "url": url,
                },
                "id":http_request.id
            }
        })

    except requests.exceptions.RequestException as e:
        # Handle requests library exceptions (e.g., network issues, timeouts)
        app.logger.error(f"RequestException occurred: {str(e)}")
        return jsonify({
            "status": 500,
            "errors": {"message": "An error occurred while making the HTTP request."},
            "data": {}
        }), 500
    except ValueError as e:
        # Handle custom validation errors or unsupported HTTP methods
        app.logger.error(f"ValueError occurred: {str(e)}")
        return jsonify({
            "status": 400,
            "errors": {"message": str(e)},
            "data": {}
        }), 400
    except Exception as e:
        # Handle other unexpected exceptions
        app.logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({
            "status": 500,
            "errors": {"message": "An unexpected error occurred."},
            "data": {}
        }), 500

if __name__ == '__main__':
    app.run()
