from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

contacts = []

# Initialize Hugging Face conversational model
chat_model = pipeline('text-generation', model='facebook/blenderbot-400M-distill')

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    contact = request.get_json()
    contact.setdefault('email', '')
    contact.setdefault('bio', '')
    contact.setdefault('profilePic', '')
    contacts.append(contact)
    return jsonify(contact), 201

@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    if id < 0 or id >= len(contacts):
        return jsonify({"error": "Contact not found"}), 404
    contact = request.get_json()
    contact.setdefault('email', '')
    contact.setdefault('bio', '')
    contact.setdefault('profilePic', '')
    contacts[id] = contact
    return jsonify(contact)

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    if id < 0 or id >= len(contacts):
        return jsonify({"error": "Contact not found"}), 404
    contact = contacts.pop(id)
    return jsonify(contact)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        input_text = data.get('input', '')
        if not input_text:
            return jsonify({'error': 'No input provided'}), 400
        response = chat_model(input_text, max_length=50, num_return_sequences=1)[0]['generated_text']
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)