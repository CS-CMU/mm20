from objects.team import Team
import map_functions
import action_handler

STARTING_ROOM = (72, 0, 255, 255)  # For testing purposes only


## This is the class which the server sees as representing the entire game
class Game(object):
    # Objects:
    # rooms: A list of all of the rooms
    # turn: Which turn it is
    # turn_limit: The maximum length the game will run
    # action_buffer: A list of actions to be performed at the next 'tick'
    # msg_buffer: A dictionary, indexed by client, of lists of responses to actions
    # teams: A list of all of the teams
    # people: A list of all of the people

    ## Called by the server to have the game set itself up
    # @param map_file
    #   the file in which the map is located
    def __init__(self, map_file):
        self.rooms = {i.name: i for i in map_functions.map_reader(map_file)}
        self.turn = 0
        # self.turn_limit = retrieveConstants("generalInfo")["TURNLIMIT"]
        self.turn_limit = 80  # For testing purposes only
        self.action_buffer = []
        self.msg_buffer = {}
        self.teams = {}
        self.people = []

    ##  Adds a new team and returns success / failure message
    # @param data
    #   The data sent by the player to set up state
    # @param client_id
    #   The ID assigned to that player by the server
    # @return
    #   A (bool, dict) tuple stating success or failure and listing errors or sending starting info to the player
    def add_new_team(self, data, client_id):
        response = {"status": "Success", "errors": []}
        try:
            newTeam = Team(data["team"], data["members"],
                           self.rooms[STARTING_ROOM], self.people)
        except KeyError:
            return (False, {"status": "Failure", "errors": ["KeyError"]})  # TODO: Make all error objects uniform
        self.msg_buffer[client_id] = []
        self.teams[client_id] = newTeam

        return (True, response)

    ## Execute queued actions
    # @return
    #   True if the game is running, False if the game ended
    def execute_turn(self):
        action_handler.handleTurn(self, self.action_buffer)
        self.action_buffer = []
        self.turn += 1
        if self.turn >= self.turn_limit:
            return False
        return True

    ## Queues all of the actions one client is attempting to execute this turn
    # @param action_list
    #   A list of actions the client wishes to perform
    # @param client_id
    #   The ID of the client sending these actions
    # @return
    #   A list of errors for invalid actions
    def queue_turn(self, action_list, client_id):
        error_list = []
        for action in action_list:
            try:
                action_handler.bufferAction(self.action_buffer, action["action"],
                                            action, client_id)
            except KeyError:
                error_list.append({"error": "invalid action",
                                   "action": action["action"]})
        return error_list

    ## Provides the information to be sent to a client each turn
    #  If the game is over, send end-of-game stuff
    # @param client_id
    #   the client to which the information will be provided
    # @return
    #   A dictionary containing the info to be sent to the player
    def get_info(self, client_id):
        #TODO: Check for end of game, then do scoring and return the winner
        response = {"warnings": [],
                    "map": self.teams[client_id].get_visible_map(),
                    "messages": self.msg_buffer[client_id]}
        self.msg_buffer[client_id] = []
        return response
