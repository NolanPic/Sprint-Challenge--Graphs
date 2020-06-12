from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Queue 

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
    # WESN -> 987 moves
    # EWSN -> 997 moves
    # SWNE -> 977 moves
    # SENW -> 996 moves
    # NSEW -> 1007 moves
    # SNEW -> 1011 moves
    # ENSW -> 1000 moves
    # NESW -> 985 moves
    # ESNW -> 996 moves
    # WSNE -> 977 moves
    # NWSE -> 1010 moves
    # WNSE -> 996 moves
    # SNWE -> 1007 moves
    # NSWE -> 1007 moves
    # NEWS -> 991 moves
    # ENWS -> 998 moves
    # WNES -> 991 moves
    # NWES -> 1001 moves
    # EWNS -> 1001 moves
    # WENS -> 996 moves
    # SWEN -> 979 moves
    # WSEN -> 987 moves
    # ESWN -> 987 moves
    # SEWN -> 981 moves
    
    return { 'room_id': room_id, 'w': '?', 's': '?', 'n': '?', 'e': '?' }

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
        
        # follow the path to the room
        for direction in path_to_next_room:
            # get the current room so that its directions
            # can be updated after the player moves
            room_id_moved_from = player.current_room.id
            player.travel(direction)
            # update the traversal path
            traversal_path.append(direction)
            # if this room has not been added to the graph, add it
            if player.current_room.id not in traversal_graph:
                traversal_graph[player.current_room.id] = build_graph_entry(player.current_room.id)
                
                # look around the room and see if there are any directions
                # that don't go anywhere. If so, mark them as None
                current_room_entry = traversal_graph[player.current_room.id]
                for key in current_room_entry:
                    if current_room_entry[key] == '?':
                        if key not in player.current_room.get_exits():
                            current_room_entry[key] = None
                            
            # update the last room's direction in the graph with this room's id
            if traversal_graph[room_id_moved_from][direction] == '?':
                update_room_exits_upon_move(direction, traversal_graph[room_id_moved_from], traversal_graph[player.current_room.id])
                
    print(traversal_graph)
    print(f'{len(traversal_graph)} rooms traversed!')
            
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
                # The room that the player is in connects
                # to an unexplored room, so there is no need
                # to do bfs to find the next unexplored room
                path_to_unexplored.append(key)
                break            
    
    if len(path_to_unexplored) == 0:
        # There are no unexplored rooms from this room--do BFS
        path_to_unexplored = bfs_to_unexplored(traversal_graph, room_entry)
    
    return path_to_unexplored
    
def bfs_to_unexplored(traversal_graph, room_entry):
    
    # create a queue of rooms
    paths = Queue()
    visited = set()
    
    paths.enqueue([room_entry['room_id']])
    
    # the path of rooms--this will be a list of room IDs to the next '?'
    correct_path = None
    while paths.size() > 0:
        path = paths.dequeue()
        
        current_room_entry_id = path[-1]
        
        if current_room_entry_id not in visited:
            visited.add(current_room_entry_id)
            
            current_room_entry = traversal_graph[current_room_entry_id]
            # look for unexplored room:
            for key in current_room_entry:
                if current_room_entry[key] == '?':
                    correct_path = path
                    break
                
            if correct_path is not None: # we have found our path, break out of BFS
                break
            
            # this is equivalent to looping through a node's neighbors
            # and adding them to the queue,
            for d in ['n', 's', 'w', 'e']:
                if current_room_entry[d] != None and current_room_entry[d] != '?':
                    copied_path = list(path)
                    copied_path.append(traversal_graph[current_room_entry[d]]['room_id'])
                    paths.enqueue(copied_path)
        
        
    # We now have the path of room IDs.
    # We need to take the path and convert
    # it into n,s,w,e directions
    directions = []
    # loop thru the correct path of room IDs
    for i in range(len(correct_path)):
        if i+1 < len(correct_path):
            # get the room and the next room
            room_id = correct_path[i]
            next_room_id = correct_path[i+1]
            room = traversal_graph[room_id]
            
            # loop thru the room and see if any
            # of its directions go to the next room.
            # If so, append that to the directions
            for d in ['n', 's', 'w', 'e']:
                if room[d] == next_room_id:
                    directions.append(d)
        
    return directions

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
