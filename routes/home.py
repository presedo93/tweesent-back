from http import HTTPStatus
from flask import Blueprint
from models.tweets import Tweets
from flask import jsonify

home = Blueprint('home', __name__)

# TWEETS_LIST = Tweets()

@home.route('/tweetlist', methods=['GET'])
def get_tweets():
  TWEETS_LIST = Tweets()
  return jsonify(TWEETS_LIST.get_tweets())