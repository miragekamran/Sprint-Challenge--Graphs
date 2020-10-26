from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Create a function called traverse and pass in player as an argument
def traverse(player):
    # Create an empty set to keep track of visited rooms
    visited = set()

    # Create an empty array to store the previouse paths
    prev_path = []

    # Loop to see those rooms that are not visited
    while len(visited) < len(world.rooms):
        # Grab the current room that the player is in and create a new var
        current_room = player.current_room
        # Grab the exits for the current room exits and create a new var
        current_room_exits = current_room.get_exits()
        # create a var for the untraversed directions from the current room
        untraversed = [direction for direction in current_room_exits if current_room.get_room_in_direction(direction) not in visited]

        # Mark the current room as visited
        visited.add(current_room)

        # if there are untraversed rooms, pick a random direction and traverse
        if untraversed:
            direction = untraversed[random.randint(0, len(untraversed) - 1)]
            player.travel(direction)
            prev_path.append(direction)
            traversal_path.append(direction)
        # othersise we are at a dead end, go to the previouse path
        else:
            # get the last direction that user went in 
            last_direction = prev_path.pop(-1)
            # reverse the last direction to go back
            reverse_direction = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}
            player.travel(reverse_direction[last_direction])
            traversal_path.append(reverse_direction[last_direction])
    
    # return tha traversal_path array
    return traversal_path

# set the traversal_path array to the traverse method and pass in the player
traversal_path = traverse(player)



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
