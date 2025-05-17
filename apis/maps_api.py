import os, aiohttp, asyncio

MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

async def _fetch_best(origin: str, destination: str, mode: str):
    params = {
        "origin":      origin,
        "destination": destination,
        "key":         os.environ['GOOGLE_MAPS_API_KEY'],
        "mode":        mode,            # only one mode per request :contentReference[oaicite:0]{index=0}
        "region":      "ca",
        "language":    "en",
        "alternatives": "false",        # only the single best route :contentReference[oaicite:1]{index=1}
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(MAPS_API_URL, params=params) as resp:
            data = await resp.json()

    routes = data.get("routes", [])
    if not routes:
        return None

    leg = routes[0]["legs"][0]
    return {
        "mode":          mode,
        "duration_text": leg["duration"]["text"],
        "duration_sec":  leg["duration"]["value"],  # compare directly in seconds
        "distance":      leg["distance"]["text"],
        "start_address": leg["start_address"],
        "end_address":   leg["end_address"],
        "steps": [
            {
                "instruction": step["html_instructions"],
                "duration":    step["duration"]["text"],
                "distance":    step["distance"]["text"],
            }
            for step in leg["steps"]
        ]
    }

async def get_directions(origin: str, destination: str):
    """
    Get directions between two locations. The LLM has later on to return the transit route. Return the walking route only if it's not far.
    :param origin: The origin location, if it's coordonates accept them latitude,langitude.
    :param destination: The destination location.
    :return: routes, origin, destination
    """
    walk, transit = await asyncio.gather(
        _fetch_best(origin, destination, "walking"),
        _fetch_best(origin, destination, "transit"),
    )

    # Filter out any that failed
    routes = [r for r in (walk, transit) if r]
    if not routes:
        return {"status": "error", "message": "no routes found"}

    return {
        "status":      "success",
        "origin":      origin,
        "destination": destination,
        "routes":      routes
    }
