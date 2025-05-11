import aiohttp
import json
import os

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

## This is a very bad api, especially in terms of output which is so long and not very relevant to the user. It costs too many tokens to use it.


async def get_news():
  """
  Get some news about what is happening in Montreal.
  :return:
  """
  params = {
      "q": "Montreal",
      "apiKey": os.environ.get('NEWS_API_KEY'),
      "language": "en",
      "sortBy": "publishedAt",
      "pageSize": 5
  }

  async with aiohttp.ClientSession() as session:
      async with session.get(NEWS_API_URL, params=params) as response:
          response_text = await response.text()
          if response.status == 200:
              data = json.loads(response_text)
              return data
