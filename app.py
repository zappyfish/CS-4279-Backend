from flask import Flask, jsonify, request
from encryption import EncryptionManager
from studies import StudyMatcher
from validation import ValidationManager
from tests import get_test_graph
from queries import *
import uuid

TEST_GRAPH_SIZE = 1000

app = Flask(__name__)

# Setup
encryption = EncryptionManager()
study_matcher = StudyMatcher()
validation = ValidationManager()
key_session_map = {}
graph = get_test_graph(TEST_GRAPH_SIZE)

@app.route('/studies/check', methods=['GET'])
def check_for_studies():
    global encryption, study_matcher, validation
    decrypted_request = encryption.decrypt(request.args)
    user_token = decrypted_request['token']
    if validation.is_valid_token(user_token):
        user_pub_key = decrypted_request['key']
        matched_studies = study_matcher.match_request_to_studies(decrypted_request)
        payload = encryption.encrypt(matched_studies, user_pub_key)
        return jsonify(payload)
    else:
        return 403


@app.route('/session/start', methods=['GET'])
def get_session_key():
    global key_session_map, graph
    key = str(uuid.uuid4())  # TODO: replace this with API key
    session = GraphSession(graph)
    key_session_map[key] = session
    return jsonify({
        'key': key
    })


@app.route('/session/check', methods=['GET'])
def continue_session():
    global key_session_map
    key = request.args.get('key')
    session = key_session_map[key]
    if 'matches' in request.args:
        splt = request.args.get('matches').split(",")
        if splt[0] != '':
            matches = [int(match) for match in splt]
        else:
            matches = []
        session.handle_response(matches)  # match numbers are comma-separated
    if session.is_done():
        print("took " + str(session.query_count) + " queries to complete")
        print(str(session.queried_node_count) + " nodes were queried out of " + str(TEST_GRAPH_SIZE))
        # remove the session
        del key_session_map[key]
        matches = session.get_matches_payload()
        # TODO: turn this into usable JSON
        return jsonify({
            'key': key,
            'done': True,
            'matches': matches,
        })
    else:
        query_form = session.get_next_query()
        return jsonify({
            'key': key,
            'done': False,
            'query': query_form,
        })


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
