import pygame
import time
from config.handle_constants import retrieveConstants
import json
from operator import itemgetter


def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

class Scoreboard(object):

    def __init__(self, **kwargs):
        self.serverDefaults = retrieveConstants("serverDefaults")
        self.constants = retrieveConstants("visualizerDefaults")
        self.SCREEN_WIDTH = self.constants["SCREEN_WIDTH"]
        self.SCREEN_HEIGHT = self.constants["SCREEN_HEIGHT"]
        self.MAX_FPS = self.constants["MAX_FPS"]
        self.TITLE = "SCOREBOARD" #TODO: move to constants file
        self.colors = self.constants["TEAMCOLORS"]
        self.running = True
        self.team_names = list()
        self.ai = list()
        self.score = list()
        self.messages = list()
        self.game_done = False
        self.game_result = None
        self.debug = kwargs.get("debug", False)
        self.quitWhenDone = self.constants['QUIT_WHEN_DONE']

        pygame.init()
        self.setup()

    def setup(self):
        pygame.display.set_caption(self.TITLE)
        self.ScreenSurface = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.GameClock = pygame.time.Clock()

    # SAM!
    # This is blindly pasted from visualizer. It looks like it should work, but check it for me?
    def run_from_file(self, file_name=""):

        # Load game log
        json_file = None
        try:
            json_file = open(file_name)
        except:
            self.running = False
            print "ERROR: Invalid game logfile."
            return

        # Run the game
        for turn_str in json_file:
            self.turn(turn_str)
            # turn_count += 1

        # If game is done and we're supposed to quit on exit, wait a while then exit
        if self.quitWhenDone:
            print "Game done; exiting"
            time.sleep(5)
            pygame.quit()

    def turn(self, turn=None):
        turn_array = json.loads(turn)
        if isinstance(turn_array[-1], int):
            turn_number = turn_array.pop()
            turn_count = turn_array.pop()
        else:
            turn_number = 0
            turn_count = 0
        while self.running and self.update_state(turn_array):
            self.draw(turn_number, turn_count)
            if self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.running = False
            if not self.game_done:
                break

    def draw(self, turn_number, turn_count):
        self.ScreenSurface.fill((0, 0, 0))
        # self.ScreenSurface.blit(self.background, (0, 0))

		# Draw AI info
        namefont = pygame.font.SysFont("monospace", 14)
        aifont = pygame.font.SysFont("monospace", 14)
        x_pos = 20
        y_pos = 10
        for i in range(len(self.ai)):
            color = self.ai[i]["COLOR"]
            label = namefont.render(self.ai[i]["TEAM NAME"], 2, color)
            # print self.team_names[i]
            # print self.colors[i]
            y_pos += 18
            self.ScreenSurface.blit(label, (x_pos, y_pos))
            x_pos2 = x_pos + 120
            for key, val in self.ai[i].iteritems():
                # print "Should be drawing"
                if not (key == "TEAM NAME" or key == "COLOR"):
                    label = aifont.render(trunc(val, 5), 1, (255, 255, 255))
                    self.ScreenSurface.blit(label, (x_pos2, y_pos))
                    x_pos2 += 120
        label = namefont.render("TEAM NAME", 2, (255, 255, 255))
        x_pos = 20
        y_pos = 10
        x_pos2 = x_pos + 120
        self.ScreenSurface.blit(label, (x_pos, y_pos))
        for key, val in self.ai[-1].iteritems():
            if not (key == "TEAM NAME" or key == "COLOR"):
                label = aifont.render(key, 1, (255, 255, 255))
                self.ScreenSurface.blit(label, (x_pos2, y_pos))
                x_pos2 += 120

        # Draw turn count
        label = aifont.render("Turn " + str(turn_number) + " of " + str(turn_count), 1, (255, 255, 255))
        self.ScreenSurface.blit(label, (x_pos, 20 * (2 + len(self.ai)) ))

        pygame.display.flip()

    def update_state(self, turn):
        # Check to see if the game has ended
        firstTurn = next(t for t in turn if t)
        if "winner" in firstTurn:
            self.game_done = True
            self.game_result = turn
            return not self.quitWhenDone
        if "team_name" in firstTurn:
            self.add_teams(turn)
            return False

        for i, player in enumerate(turn):

            # Skip bad teams
            if not player or player.get("status") == "Failure":
                continue

            self.ai[i] = player["aiStats"]
            self.score[i] = player["score"]
            self.ai[i]["Final Score"] = self.score[i]
            self.ai[i]["TEAM NAME"] = self.team_names[i]
            self.ai[i]["COLOR"] = self.colors[-1]
            if len(self.colors) > i:
                self.ai[i]["COLOR"] = self.colors[i]

        self.ai = sorted(self.ai, key=lambda k: -1*k["Final Score"])
            # self.ai = sorted(self.ai, key=itemgetter('Final Score')) 


        return True


    # Initialization of the teams
    def add_teams(self, teams):
        """
        set up the visualizer to view the teams
        """

        # Remove null teams (due to bad clients)
        self.ai = [None] * len(teams)
        self.score = [None] * len(teams)
        self.team_names = list(self.ai)
        number_of_people = 0

        for i, player in enumerate(teams):
            if player and player.get("status", "Failure") != "Failure":
                self.team_names[i] = player["team_name"]
                number_of_people += len(player["team"])
            else:
                self.team_names[i] = ""


if __name__ == "__main__":
    mapConstants = retrieveConstants("serverDefaults")
    mapPath = mapConstants['map']
    score = Scoreboard()
    score.run_from_file(("serverlog.json"))
