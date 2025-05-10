from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

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

if __name__ == '__main__':
    logger.info("Starting Flask server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)