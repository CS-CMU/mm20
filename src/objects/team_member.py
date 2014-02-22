class TeamMember(object):

    def __init__(self, name, archetype, location):
        """
        Initializes a team member object with name, archetype, and coordinates
        for being placed on the map.
        location: room the player currently is in
        """

        self.energy = 100
        self.name = name
        self.archetype = archetype
        self.location = location

    def move(destination):
        """
        Moves the player to the desired room
        How will this be worked out visually, pathfinding?
        """
        self.location = destinations

    def eat(foodTable):
        """
        Adjusts player's stats based on what foods are eaten
        What stats need to be added/changed?
        """
        self.energy += foodTable.food.energyValue
        foodTable.amount -= 1

    def sleep(hours):
        """
        Adjusts player's energy based on how long they sleep for
        """
        self.energy += (hours * 15)

    def code(ai):
        """
        Adjusts ai's stats. should probably accept some argument that
        says which stats to adjust and in what way
        """
        print "not yet implemented"
    


#this is how you can do simple tests
if __name__ == "__main__":
    sam = TeamMember("Sam", "Coder", "2405")
    print sam.energy
    print sam.name
    print sam.archetype
    print sam.location