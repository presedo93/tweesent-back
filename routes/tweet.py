import tweepy


class TweeterBack:
  def __init__(self):
    # Twitter Api Credentials
    consumerKey = "IOUuOWRk0DQiFzPcilzEDvJfU"
    consumerSecret = "Fe4fzMbq4ixXM2qp2wOqrqyTXyuBMuPyXCG7s0nPzVcge7FtKl"
    accessToken = "1329499640773943297-cBwv4waJK5wGzat1jCUcw7pt4qOwOb"
    accessTokenSecret = "6ZmaNh8NQpgB0FDvX2aQIsAgQxf9Lk7JA2bU1VmCJiH4x"

    # Create the authentication object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret)

    # Creating the API object while passing in auth information
    self.api = tweepy.API(authenticate, wait_on_rate_limit = True)

  def search(self, input : str, count: int = 50):

    posts = self.api.search(q=input, count=count, lang="es", tweet_mode="extended")

    #  Print the last 5 tweets
    print("Show the 5 recent tweets:\n")
    i=1
    for tweet in posts[:5]:
        # print(str(i) +') '+ tweet.full_text + '\n')
        print(tweet.full_text)
        print('***')
        i= i+1
  def get_model(self):
    return self