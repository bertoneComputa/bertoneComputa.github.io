from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from threading import Lock
import uuid
import shutil

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File for persistent storage
REPO_CONTACTS_FILE = 'contacts.txt'
VERCEL_CONTACTS_FILE = '/tmp/contacts.txt'
CONTACTS_FILE = VERCEL_CONTACTS_FILE if os.getenv('VERCEL') else REPO_CONTACTS_FILE
file_lock = Lock()

def load_contacts():
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            contact_id, name, phone, email, bio, profilePic = line.split('|', 5)
                            contacts.append({
                                'id': contact_id,
                                'name': name,
                                'phone': phone,
                                'email': email,
                                'bio': bio,
                                'profilePic': profilePic
                            })
                        except ValueError:
                            logger.warning(f"Skipping malformed line in {CONTACTS_FILE}: {line}")
        except Exception as e:
            logger.error(f"Error loading contacts from {CONTACTS_FILE}: {str(e)}")
    # If on Vercel, copy contacts.txt to repo for persistence
    if os.getenv('VERCEL') and os.path.exists(CONTACTS_FILE):
        try:
            shutil.copy(CONTACTS_FILE, REPO_CONTACTS_FILE)
        except Exception as e:
            logger.warning(f"Failed to copy {CONTACTS_FILE} to {REPO_CONTACTS_FILE}: {str(e)}")
    return contacts

def save_contacts(contacts):
    try:
        with file_lock:
            with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
                for contact in contacts:
                    f.write(f"{contact['id']}|{contact['name']}|{contact['phone']}|{contact['email']}|{contact['bio']}|{contact['profilePic']}\n")
        # If on Vercel, copy to repo contacts.txt
        if os.getenv('VERCEL'):
            try:
                shutil.copy(CONTACTS_FILE, REPO_CONTACTS_FILE)
            except Exception as e:
                logger.warning(f"Failed to copy {CONTACTS_FILE} to {REPO_CONTACTS_FILE}: {str(e)}")
    except Exception as e:
        logger.error(f"Error saving contacts to {CONTACTS_FILE}: {str(e)}")
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
        if not contact.get('name') or not contact.get('phone'):
            return jsonify({"error": "Name and phone are required"}), 400
        logger.info(f"Adding contact: {contact}")
        contact.setdefault('email', '')
        contact.setdefault('bio', '')
        contact.setdefault('profilePic', '')
        contact['id'] = str(uuid.uuid4())
        contacts.append(contact)
        save_contacts(contacts)
        return jsonify(contact), 201
    except Exception as e:
        logger.error(f"Error adding contact: {str(e)}")
        return jsonify({"error": f"Failed to save contact: {str(e)}"}), 500

@app.route('/api/contacts/<string:id>', methods=['PUT'])
def update_contact(id):
    try:
        contact = request.get_json()
        if not contact.get('name') or not contact.get('phone'):
            return jsonify({"error": "Name and phone are required"}), 400
        logger.info(f"Updating contact ID {id}: {contact}")
        for i, c in enumerate(contacts):
            if c['id'] == id:
                contact.setdefault('email', '')
                contact.setdefault('bio', '')
                contact.setdefault('profilePic', '')
                contact['id'] = id
                contacts[i] = contact
                save_contacts(contacts)
                return jsonify(contact)
        logger.warning(f"Contact ID {id} not found")
        return jsonify({"error": "Contact not found"}), 404
    except Exception as e:
        logger.error(f"Error updating contact: {str(e)}")
        return jsonify({"error": f"Failed to update contact: {str(e)}"}), 500

@app.route('/api/contacts/<string:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        for i, c in enumerate(contacts):
            if c['id'] == id:
                contact = contacts.pop(i)
                logger.info(f"Deleted contact ID {id}: {contact}")
                save_contacts(contacts)
                return jsonify(contact)
        logger.warning(f"Contact ID {id} not found")
        return jsonify({"error": "Contact not found"}), 404
    except Exception as e:
        logger.error(f"Error deleting contact: {str(e)}")
        return jsonify({"error": f"Failed to delete contact: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info("Starting Flask server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)