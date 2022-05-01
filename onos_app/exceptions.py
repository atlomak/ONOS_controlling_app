#Exceptions
class OnosControllerError(Exception):
    """Failed to create Controller object"""
class OnosWrongAuth(Exception):
    """The credentials provided are invalid"""
class OnosHostsError(Exception):
    """Failed to load Hosts"""
class OnosSwitchError(Exception):
    """Failed to load Switches"""
class OnosWrongIP(Exception):
    """The Host's ip provied is invalid"""