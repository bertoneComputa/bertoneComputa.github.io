from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import json
import os
from threading import Lock

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File for persistent storage
CONTACTS_FILE = 'contacts.json'
file_lock = Lock()

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading contacts from file: {str(e)}")
            return []
    return []

def save_contacts(contacts):
    try:
        with file_lock:
            with open(CONTACTS_FILE, 'w') as f:
                json.dump(contacts, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving contacts to file: {str(e)}")
        raise

contacts = load_contacts()

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
        save_contacts(contacts)
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
        save_contacts(contacts)
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
        save_contacts(contacts)
        return jsonify(contact)
    except Exception as e:
        logger.error(f"Error deleting contact: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)