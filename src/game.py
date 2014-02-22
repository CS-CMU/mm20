from objects.room import Room
from objects.team import Team
from objects.team_member import TeamMember
from map_functions import map_reader

class Game(object):

    def __init__(self, map_file_url):
        """
        This is called once to init the server
        the map reader will return a list of rooms that have been
        linked together as defined in the design doc. 
        """
        rooms = map_reader(file_url)
        
    def add_new_team():
        pass