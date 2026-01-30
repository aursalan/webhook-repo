from flask import Blueprint, jsonify, request
from datetime import datetime
from ..extensions import mongo

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def handle_webhook():
    # 1. Get the Event Type
    event_type = request.headers.get('X-GitHub-Event')
    data = request.json
    payload = None

    # 2. PUSH Logic
    if event_type == 'push':
        if data.get('deleted') is True: # Ignore deletions
            return jsonify({"msg": "Ignored deletion"}), 200

        payload = {
            "request_id": data['head_commit']['id'], # Commit Hash
            "author": data['pusher']['name'],
            "action": "PUSH",
            "from_branch": data['ref'].split('/')[-1], 
            "to_branch": data['ref'].split('/')[-1],
            "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
        }

    # 3. PULL REQUEST & MERGE Logic
    elif event_type == 'pull_request':
        action = data.get('action')
        pr = data['pull_request']

        # Brownie Point: MERGE action (closed + merged=True)
        if action == 'closed' and pr.get('merged'):
            payload = {
                "request_id": str(pr['id']), # PR ID
                "author": pr['user']['login'],
                "action": "MERGE",
                "from_branch": pr['head']['ref'],
                "to_branch": pr['base']['ref'],
                "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            }
        
        # Standard Open PR
        elif action == 'opened':
            payload = {
                "request_id": str(pr['id']),
                "author": pr['user']['login'],
                "action": "PULL_REQUEST",
                "from_branch": pr['head']['ref'],
                "to_branch": pr['base']['ref'],
                "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            }

    # 4. Insert into MongoDB
    if payload:
        # Access the 'events' collection in the 'techstax_db' database
        mongo.db.events.insert_one(payload)
        return jsonify({"msg": "Event stored"}), 201

    return jsonify({"msg": "Action ignored"}), 200