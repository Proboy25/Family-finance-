from flask import request, jsonify
from . import app, db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }

with app.app_context():
    db.create_all()

@app.route('/clients', methods=['GET'])
def list_clients():
    clients = Client.query.all()
    return jsonify([c.to_dict() for c in clients])

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json(force=True)
    client = Client(name=data['name'], email=data['email'], phone=data.get('phone'))
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

@app.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return '', 204
