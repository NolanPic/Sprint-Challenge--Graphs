from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
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

def build_graph_entry(room_id):
    return { 'room_id': room_id, 'n': '?', 's': '?', 'w': '?', 'e': '?' }

def dft():
    rooms_count = len(room_graph) # count up to this when building our traversal graph
    # build a traversal graph as we go
    # do dft and build the graph
    # in each room, track the direction you take next in traversal_path
    # figure out backtracking for unexplored areas of the graph
    
    # do DFT until you reach a dead end
    # do BFS to find a '?'
    # The BFS should return a path of n,s,w,e directions that the main DFT can pick back up on
    
    traversal_graph = {}
    
    traversal_graph[player.current_room.id] = build_graph_entry(player.current_room.id)
    
    # while our traversal graph is not complete,  
    
    while len(traversal_graph) != rooms_count:
    
        # get the path to the next room
        path_to_next_room = path_to_next_unexplored_room(traversal_graph, traversal_graph[player.current_room.id], player.current_room)
        
        # for testing
        if len(path_to_next_room) == 0:
            break
        
        # follow the path to the room
        for direction in path_to_next_room:
            # get the current room so that its directions
            # can be updated after the player moves
            room_id_moved_from = player.current_room.id
            print("Travelled to room:")
            player.travel(direction, show_rooms=True)
            # if this room has not been added to the graph, add it
            if player.current_room.id not in traversal_graph:
                traversal_graph[player.current_room.id] = build_graph_entry(player.current_room.id)
            # update the last room's direction in the graph with this room's id
            if traversal_graph[room_id_moved_from][direction] == '?':
                update_room_exits_upon_move(direction, traversal_graph[room_id_moved_from], traversal_graph[player.current_room.id])
            
        print(traversal_graph)
            
def update_room_exits_upon_move(direction_moved, moved_from_room_entry, moved_to_room_entry):
    # get the opposite direction to update the room you went to
    opposites = { 'n': 's', 's': 'n', 'w': 'e', 'e': 'w' }
    opposite_dir = opposites[direction_moved]
    
    # update the room directions
    moved_from_room_entry[direction_moved] = moved_to_room_entry["room_id"]
    moved_to_room_entry[opposite_dir] = moved_from_room_entry["room_id"]
    
def path_to_next_unexplored_room(traversal_graph, room_entry, room):
    path_to_unexplored = []
    for key in room_entry:
        if room_entry[key] == '?':
            if key in room.get_exits(): # ensure player can move to this room
                # the room that the player is in connects
                # to an unexplored room, so there is no need
                # to do bfs to find the next unexplored room
                path_to_unexplored.append(key)
                break
            else:
                # this path does not exist--update graph with 'None' for this dir
                # so a visit won't be attempted again
                traversal_graph[room.id][key] = None             
    
    #if len(path_to_unexplored) == 0:
        # no unexplored rooms from this room--do BFS
        #path_to_unexplored = bfs_to_unexplored(traversal_graph, room_entry)
    
    return path_to_unexplored
    
def bfs_to_unexplored(traversal_graph, room_entry):
    if room_entry is None:
        room_entry = traversal_graph[0]
    
    # create a queue of rooms
    paths = []
    visited = set()
    
    paths.append([room_entry])
    
    while len(paths) > 0:
        path = paths.pop(0)
        
        current_room_entry = path[-1]
        
        if current_room_entry.room_id not in visited:
            visited.add(current_room_entry.room_id)
            
            # look for unexplored room:
            for key in current_room_entry:
                if current_room_entry[key] == '?':
                    return path_to_unexplored


dft()


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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
