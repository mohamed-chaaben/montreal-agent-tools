import praw
import os
from datetime import datetime

reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     user_agent="python.montreal.agent",
                     username="harmonic-mean",
                     password=os.environ['REDDIT_PASSWORD'])


async def get_reddit():
  """
Returns the 10 hottest posts from the r/montreal subreddit. This is to serve the LLM which has later on to choose if any of these posts are relevant to the user, in this case it returns a list of the is of those releant posts.
  """
  return [{
      "title": submission.title,
      "score": submission.score,
      "id": submission.id,
      "num_comments": submission.num_comments,
      "created": datetime.fromtimestamp(submission.created).__str__(),
  } for submission in reddit.subreddit("montreal").hot(limit=10)]
