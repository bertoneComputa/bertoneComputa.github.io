from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

contacts = []

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    contact = request.get_json()
    # Ensure optional fields are handled
    contact.setdefault('email', '')
    contact.setdefault('bio', '')
    contact.setdefault('profilePic', '')
    contacts.append(contact)
    return jsonify(contact), 201

@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = request.get_json()
    # Ensure optional fields are handled
    contact.setdefault('email', '')
    contact.setdefault('bio', '')
    contact.setdefault('profilePic', '')
    contacts[id] = contact
    return jsonify(contact)

@app.route('/api/contcasts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = contacts.pop(id)
    return jsonify(contact)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)