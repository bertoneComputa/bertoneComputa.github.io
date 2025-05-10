from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

contacts = []

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    logger.info("Fetching all contacts")
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    try:
        contact = request.get_json()
        logger.info(f"Adding contact: {contact}")
        contact.setdefault('email', '')
        contact.setdefault('bio', '')
        contact.setdefault('profilePic', '')
        contacts.append(contact)
        return jsonify(contact), 201
    except Exception as e:
        logger.error(f"Error adding contact: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    try:
        if id < 0 or id >= len(contacts):
            logger.warning(f"Contact ID {id} not found")
            return jsonify({"error": "Contact not found"}), 404
        contact = request.get_json()
        logger.info(f"Updating contact ID {id}: {contact}")
        contact.setdefault('email', '')
        contact.setdefault('bio', '')
        contact.setdefault('profilePic', '')
        contacts[id] = contact
        return jsonify(contact)
    except Exception as e:
        logger.error(f"Error updating contact: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        if id < 0 or id >= len(contacts):
            logger.warning(f"Contact ID {id} not found")
            return jsonify({"error": "Contact not found"}), 404
        contact = contacts.pop(id)
        logger.info(f"Deleted contact ID {id}: {contact}")
        return jsonify(contact)
    except Exception as e:
        logger.error(f"Error deleting contact: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        input_text = data.get('input', '')
        logger.info(f"Chat input: {input_text}")
        if not input_text:
            logger.warning("No input provided for chat")
            return jsonify({'error': 'No input provided'}), 400
        
        # Proxy request to JSONPlaceholder
        response = requests.get('https://jsonplaceholder.typicode.com/users/1')
        if response.status_code != 200:
            logger.error(f"JSONPlaceholder API error: {response.status_code}")
            return jsonify({'error': 'Failed to fetch data from API'}), 500
        
        user_data = response.json()
        logger.info(f"JSONPlaceholder response: {user_data}")
        return jsonify({
            'name': user_data.get('name', 'Unknown'),
            'phone': user_data.get('phone', 'No phone')
        })
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)