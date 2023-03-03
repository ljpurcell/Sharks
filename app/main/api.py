from flask import request, make_response
from . import api


@api.route('/votes', methods=['POST'])
def post_votes():
    req = request.get_json()
    print(req)