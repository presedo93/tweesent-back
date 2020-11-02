from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/mensaje')
def create_task():
    return jsonify('Data from Flask')

COUNT = 0
TWEETS = ['Tweet 1', 'Tweet 2']

@app.route('/tweetlist')
def get_tweets():
    global TWEETS
    return jsonify(TWEETS)


@app.route('/getcount')
def get_counter():
    global COUNT
    return jsonify(COUNT)

@app.route('/setcount', methods=['GET', 'POST'])
def set_counter():
    global COUNT
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        COUNT = int(post_data.get('data'))
        response_object['message'] = 'Counter updated!'
    else:
        response_object['books'] = BOOKS
    return jsonify(COUNT)


@app.route('/addfive', methods=['POST'])
def addfive_counter():
    global COUNT
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        COUNT = int(post_data.get('data')) + 5
        response_object['message'] = 'Counter updated!'
    else:
        response_object['books'] = BOOKS
    return jsonify(COUNT)


@app.route('/subfive', methods=['POST'])
def subfive_counter():
    global COUNT
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        COUNT = int(post_data.get('data')) - 5
        response_object['message'] = 'Counter updated!'
    else:
        response_object['books'] = BOOKS
    return jsonify(COUNT)


if __name__ == '__main__':
    app.run(debug=True)