from flask import Flask, request, jsonify
import pyreadstat
import os
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch UUID_SECRET from environment variables
UUID_SECRET = os.getenv('UUID_SECRET')

# Function to check UUID in the request headers
def authenticate(request):
    # Retrieve the UUID from the request headers
    user_uuid = request.headers.get('USER-UUID')
    
    if user_uuid != UUID_SECRET:
        return False  # If the UUID doesn't match, authentication fails
    return True

@app.route('/get_headers', methods=['POST'])
def get_headers():
    # Authenticate the request using the UUID
    if not authenticate(request):
        return jsonify({"error": "Unauthorized. Invalid UUID."}), 401

    # Check if the file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    # Check if the file has the correct extension
    if not file.filename.endswith('.sav'):
        return jsonify({"error": "File format not supported. Please upload a .sav file."}), 400

    try:
        # Save the uploaded file temporarily
        temp_file_path = os.path.join("temp.sav")
        file.save(temp_file_path)

        # Read the .sav file to extract headers
        df, meta = pyreadstat.read_sav(temp_file_path)
        headers = list(df.columns)

        # Delete the temporary file after reading
        os.remove(temp_file_path)
        
        # Return the headers in JSON format
        return jsonify({"headers": headers})
    
    except Exception as e:
        # Handle any errors that occur
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
