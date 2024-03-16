from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://uk.indeed.com"}})

# Load existing data from JSON file
try:
    with open('records.json', 'r') as file:
        json_data = json.load(file)
except FileNotFoundError:
    json_data = []


@app.route('/check-id', methods=['POST'])
def check_id():
    data = request.json
    record_id = data.get('id')

    # Check if the record ID is present in the JSON file
    is_present = is_record_present(record_id)
    
    if is_present:
        response = {"status": "success", "message": "ID present"}
    else:
        response = {"status": "success", "message": "ID not present"}

    return jsonify(response)


@app.route('/extract-info', methods=['POST'])
def extract_info():
    data = request.json
    job_title = data.get('title')
    record_id = data.get('id')
    company = data.get('company')
    location = data.get('location')
    rate = data.get('rate')


    # Check if the record ID is present in the JSON file
    is_present = is_record_present(record_id)

    if not is_present:
        # If not present, add the information to the JSON file
        
        web_app_url = 'https://script.google.com/macros/s/AKfycbzqFTktklZKiqM8aHDfO5b91F_buZLpeHYwuFvwCPpyu7SSCq5du_XYGvDR0Rj7BdzW/exec'
        
        response = requests.post(web_app_url, json = data)
        response = {"status": "success", "message": "Record added and JSON file updated"}
        json_data.append(record_id)

        # Update the JSON file
        with open('records.json', 'w') as file:
            json.dump(json_data, file)
    else:
        response = {"status": "success", "message": "Record already present"}

    return jsonify(response)


def is_record_present(record_id):
    return record_id in json_data



if __name__ == '__main__':
    app.run(port=5000)