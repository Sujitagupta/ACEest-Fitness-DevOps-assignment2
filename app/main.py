from flask import Flask, jsonify, request, abort
import os
from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config['APP_VERSION'] = os.getenv('APP_VERSION', 'v1.0')

    # In-memory datastore (merged from versions)
    members = [
        {"id": 1, "name": "Alice", "membership": "Gold"},
        {"id": 2, "name": "Bob", "membership": "Silver"}
    ]
    classes = [
        {"id": 1, "name": "Yoga", "slots": 10},
        {"id": 2, "name": "CrossFit", "slots": 8}
    ]
    bookings = []  # simple booking record list

    @app.route('/')
    def index():
        return jsonify({
            "app": "ACEest Fitness & Gym",
            "version": app.config['APP_VERSION'],
            "time": datetime.utcnow().isoformat() + "Z"
        })

    @app.route('/health')
    def health():
        return jsonify({"status": "ok", "version": app.config['APP_VERSION']})

    # Members endpoints
    @app.route('/members', methods=['GET'])
    def get_members():
        return jsonify(members)

    @app.route('/members/<int:member_id>', methods=['GET'])
    def get_member(member_id):
        m = next((x for x in members if x['id'] == member_id), None)
        if not m:
            abort(404)
        return jsonify(m)

    @app.route('/members', methods=['POST'])
    def create_member():
        data = request.get_json()
        if not data or 'name' not in data:
            abort(400)
        new_id = max(m['id'] for m in members) + 1 if members else 1
        member = {"id": new_id, "name": data['name'], "membership": data.get('membership', 'Basic')}
        members.append(member)
        return jsonify(member), 201

    @app.route('/members/<int:member_id>', methods=['PUT'])
    def update_member(member_id):
        data = request.get_json()
        if not data:
            abort(400)
        m = next((x for x in members if x['id'] == member_id), None)
        if not m:
            abort(404)
        m.update({k:v for k,v in data.items() if k in ['name','membership']})
        return jsonify(m)

    @app.route('/members/<int:member_id>', methods=['DELETE'])
    def delete_member(member_id):
        nonlocal members
        m = next((x for x in members if x['id'] == member_id), None)
        if not m:
            abort(404)
        members = [x for x in members if x['id'] != member_id]
        return jsonify({"deleted": member_id})

    # Classes endpoints
    @app.route('/classes', methods=['GET'])
    def get_classes():
        return jsonify(classes)

    @app.route('/classes/<int:class_id>/book', methods=['POST'])
    def book_class(class_id):
        c = next((x for x in classes if x['id'] == class_id), None)
        if not c:
            abort(404)
        if c['slots'] <= 0:
            return jsonify({"error": "full"}), 400
        c['slots'] -= 1
        booking = {"id": len(bookings)+1, "class_id": class_id, "time": datetime.utcnow().isoformat()+"Z"}
        bookings.append(booking)
        return jsonify({"message": "booked", "booking": booking})

    @app.route('/bookings', methods=['GET'])
    def get_bookings():
        return jsonify(bookings)

    # Simple metrics endpoint
    @app.route('/metrics', methods=['GET'])
    def metrics():
        return jsonify({
            "members_count": len(members),
            "classes_count": len(classes),
            "bookings_count": len(bookings)
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
