from flask import Blueprint, json, request, jsonify
from box import Box
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/push', methods=["POST"])
def receiver():
    data = request.get_json()
    obj = Box(data)

    if data is None:
        return jsonify({"error":"Invalid Json Format"}),400

    print(f'request_id:{obj.pull_request.head.sha},request:{obj.action},author:{obj.pull_request.user.login},from_branch:{obj.pull_request.head.ref},to_branch:')

    print(f'YOUR Default Branch ID IS {obj.pull_request.head.repo.default_branch}')
    print(f'Time Stamp: Created_At:{obj.pull_request.created_at}, Updated_At:{obj.pull_request.updated_at}')
    return jsonify(data),200