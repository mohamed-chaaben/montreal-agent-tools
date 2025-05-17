def get_location(location=None):
    """
    This function should be used when the user location is needed.
    :param location: A dummy variable
    :return the string 'LOCATION_REQUEST_SIGNAL' as a signal to trigger the app to ask the user for his location.
    """
    if location is None:
        return "LOCATION_REQUEST_SIGNAL"
    return location
