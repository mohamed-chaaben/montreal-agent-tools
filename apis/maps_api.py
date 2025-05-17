import os, aiohttp, asyncio
from datetime import datetime

MAPS_API_URL = "https://maps.googleapis.com/maps/api/directions/json"

async def _fetch_best(origin: str, destination: str, mode: str):
    params = {
        "origin":       origin,
        "destination":  destination,
        "key":          os.environ['GOOGLE_MAPS_API_KEY'],
        "mode":         mode,            # only one mode per request :contentReference[oaicite:0]{index=0}
        "region":       "ca",
        "language":     "en",
        "alternatives": "false",         # only the single best route :contentReference[oaicite:1]{index=1}
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(MAPS_API_URL, params=params) as resp:
            data = await resp.json()

    routes = data.get("routes", [])
    if not routes:
        return None

    leg = routes[0]["legs"][0]

    # Transit legs include departure_time and arrival_time objects;
    # for walking we’ll default departure to “now” and arrival = now + duration
    dep = leg.get("departure_time", {})
    arr = leg.get("arrival_time", {})

    if mode == "walking":
        departure_time_text = datetime.now().strftime("%I:%M %p")
        arrival_time_text   = arr.get("text") or ""  # often not provided for walking
    else:
        departure_time_text = dep.get("text", "")
        arrival_time_text   = arr.get("text", "")

    return {
        "mode":                 mode,
        "departure_time_text":  departure_time_text,
        "arrival_time_text":    arrival_time_text,
        "duration_text":        leg["duration"]["text"],
        "duration_sec":         leg["duration"]["value"],
        "distance":             leg["distance"]["text"],
        "start_address":        leg["start_address"],
        "end_address":          leg["end_address"],
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
    Returns exactly two routes:
      1) best walking route (with departure_time_text = now)
      2) best transit route (with departure_time_text from the API)
    """
    walk, transit = await asyncio.gather(
        _fetch_best(origin, destination, "walking"),
        _fetch_best(origin, destination, "transit"),
    )

    routes = [r for r in (walk, transit) if r]
    if not routes:
        return {"status": "error", "message": "no routes found"}

    return {
        "status":      "success",
        "origin":      origin,
        "destination": destination,
        "routes":      routes
    }
