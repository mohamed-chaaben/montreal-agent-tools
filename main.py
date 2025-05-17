from fastmcp import FastMCP


from apis.reddit_api import get_reddit
from apis.maps_api import get_directions
from apis.news_api import get_news
from apis.weather_api import get_weather
from apis.need_location import get_location


mcp = FastMCP('Demo')

get_weather = mcp.tool()(get_weather)
get_news = mcp.tool()(get_news)
get_directions = mcp.tool()(get_directions)
get_reddit = mcp.tool()(get_reddit)
get_location = mcp.tool()(get_location)



if __name__ == '__main__':
    mcp.run(transport='sse', host='0.0.0.0', port=8000)
