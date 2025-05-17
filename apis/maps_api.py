import os
import aiohttp

MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"


async def get_directions(origin: str, destination: str):
    """
    Get directions between two locations. The LLM has later on to return the best route, not all of them.
    :param origin: The origin location, if it's coordonates accept them latitude,langitude.
    :param destination: The destination location.
    :return: routes, origin, destination
    """
    params = {
        "origin": origin,
        "destination": destination,
        "key": os.environ.get('GOOGLE_MAPS_API_KEY'),
        "mode": "transit",
        "region": "ca",
        "language": "en",
        "alternatives": "true"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(MAPS_API_URL, params=params) as response:
            data = await response.json()

        routes = []
        for route in data.get("routes", []):
            legs = route.get("legs", [{}])[0]
            route_info = {
                "summary": route.get("summary", ""),
                "duration": legs.get("duration", {}).get("text", ""),
                "distance": legs.get("distance", {}).get("text", ""),
                "start_address": legs.get("start_address", ""),
                "end_address": legs.get("end_address", ""),
                "steps": []
            }
            for step in legs.get("steps", []):
                transit_details = step.get("transit_details", {})
                step_info = {
                    "instruction":
                    step.get("html_instructions", ""),
                    "duration":
                    step.get("duration", {}).get("text", ""),
                    "distance":
                    step.get("distance", {}).get("text", ""),
                    "transit_line":
                    transit_details.get("line", {}).get("name", ""),
                    "transit_stops":
                    transit_details.get("num_stops", 0),
                    "departure_stop":
                    transit_details.get("departure_stop", {}).get("name", ""),
                    "arrival_stop":
                    transit_details.get("arrival_stop", {}).get("name", "")
                }
                route_info["steps"].append(step_info)

            routes.append(route_info)

        return {
            "status": "success",
            "routes": routes,
            "origin": origin,
            "destination": destination
        }
