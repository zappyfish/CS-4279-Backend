from flask import Flask, jsonify, request
from encryption import EncryptionManager
from studies import StudyMatcher
from validation import ValidationManager

# Setup
encryption = EncryptionManager()
study_matcher = StudyMatcher()
validation = ValidationManager()

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run()