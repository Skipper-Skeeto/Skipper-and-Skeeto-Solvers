import random
import os

class Room:
    def __init__(self, connected_rooms, required_items):   
        self.connected_rooms = connected_rooms
        self.required_items = required_items

class Item:
    def __init__(self, room, required_items):   
        self.room = room
        self.required_items = required_items
        self.active = True

class Skipper (object):
    def __init__(self):
        self.rooms = {}
        self.items = {}
        self.inventory = []
        self.current_room = "main_hall"
        self.previous_room = "null"
        self.current_moves = 0
        self.best_win = 999
        self.max_moves = 80
        self.total_attempts = 0
    
    def reset (self):
        self.current_moves = 0
        self.current_room = "main_hall"
        self.previous_room = "null"
        self.inventory = []

        self.rooms = {
            "main_hall": Room(["library", "kitchen", "first_floor", "dining_room", "tower_1"], None),
            "library": Room(["main_hall", "laboratory"], None),
            "laboratory": Room(["library"], ["blue_book", "matchbox"]),
            "kitchen": Room(["main_hall", "greenhouse", "wine_cellar"], None),
            "greenhouse": Room(["kitchen"], ["rubber_band", "slingshot_handle"]),
            "wine_cellar": Room(["kitchen", "barrel_room"], None),
            "barrel_room": Room(["wine_cellar", "sewer_1"], ["bottle_1", "bottle_2", "bottle_3", "hammer_head", "hammer_handle", "battery", "rabbit", "nitro"]),
            "sewer_1": Room(["barrel_room", "sewer_2"], None),
            "sewer_2": Room(["treasure_chamber", "sewer_1"], ["ladder_key", "old_ghost"]),
            "treasure_chamber": Room(["finish"], None),
            "finish": Room(None, None),
            "dining_room": Room(["main_hall", "dining_room_table"], ["tall_flower", "dining_room_key", "dining_ghost"]),
            "dining_room_table": Room(["dining_room"], ["spring"]),
            "tower_1": Room(["main_hall", "crypt", "tower_2"], ["tower_key"]),
            "crypt": Room(["tower_1"], ["medallion", "wick", "matchbox"]),
            "tower_2": Room(["tower_1", "girls_room"], None),
            "girls_room": Room(["tower_2", "clockworks"], ["lever"]),
            "clockworks": Room(["girls_room"], None),
            "first_floor": Room(["main_hall", "observatory", "bedroom", "skull_stairs", "hunting_room", "guest_room", "counts_room"], None),
            "observatory": Room([ "first_floor"], None),
            "bedroom": Room(["first_floor"], ["bedroom_key_1", "bedroom_key_2"]),
            "skull_stairs": Room(["first_floor", "fake_treasure_room"], ["green_ghost"]),
            "fake_treasure_room": Room(["skull_stairs"], None),
            "hunting_room": Room(["first_floor", "mouse_door"], ["hunting_ghost"]),
            "mouse_door": Room(["hunting_room"], ["dentures"]),
            "guest_room": Room(["first_floor"], None),
            "counts_room": Room(["first_floor", "lumber_room"], None),
            "lumber_room": Room(["counts_room"], ["girl_ghost"])
        }

        self.items = {
            "medallion": Item("main_hall", None),
            "matchbox": Item("main_hall", None),
            "tower_key": Item("library", None),
            "nitro": Item("laboratory", None),
            "spoon": Item("kitchen", None),
            "wick": Item("kitchen", None),
            "tall_flower": Item("greenhouse", None),
            "doll_head": Item("wine_cellar", None),
            "bedroom_key_1": Item("dining_room", None),
            "dentures": Item("dining_room_table", None),
            "bottle_1": Item("dining_room_table", None),
            "green_ghost": Item("crypt", ["penny"]),
            "dining_ghost": Item("crypt", ["spoon"]),
            "girl_ghost": Item("crypt", ["doll_head", "doll_body"]),
            "old_ghost": Item("crypt", ["needle"]),
            "hunting_ghost": Item("crypt", ["bugle"]),
            "hammer_head": Item("tower_1", None),
            "battery": Item("tower_2", None),
            "doll_body": Item("girls_room", None),
            "spring": Item("clockworks", None),
            "bedroom_key_2": Item("first_floor", None),
            "ladder_key": Item("observatory", None),
            "rubber_band": Item("observatory", None),
            "needle": Item("bedroom", None),
            "bottle_2": Item("fake_treasure_room", None),
            "bottle_3": Item("hunting_room", None),
            "penny": Item("mouse_door", None),
            "rabbit": Item("mouse_door", None),
            "hammer_handle": Item("guest_room", None),
            "blue_book": Item("guest_room", None),
            "lever": Item("counts_room", None),
            "slingshot_handle": Item("counts_room", None),
            "dining_room_key": Item("counts_room", None),
            "bugle": Item("lumber_room", None)
        }

    def loop (self):
        reset = True
        output = ""
        while True:
            if reset:
                os.system('cls')
                print("SKIPPER AND SKEETO 2 SOLVER")
                print("===========================")
                print(f"Total Attempts: {self.total_attempts}")
                print(f"Best Win (Least Moves): {self.best_win}")
                self.total_attempts += 1
                output = ""
                reset = False
                self.reset()
            room_choices = []
            hasPerformedAction = False

            # Gather all possible collectable items in the room
            for key, value in self.items.items():
                if value.room is self.current_room:
                    canGetItem = True
                    if value.required_items is not None:
                        for i in value.required_items:
                            if not i in self.inventory:
                                canGetItem = False
                    if canGetItem and value.active:
                        self.inventory.append(key)
                        value.active = False
                        output += (f"- Picked up {key}\n")
                        hasPerformedAction = True

            # Pick a random room out of all possible exits (excluding where the bot came in)
            for room in self.rooms[self.current_room].connected_rooms:
                canEnterRoom = True
                if room in self.rooms:
                    if self.rooms[room].required_items is not None:
                        for i in self.rooms[room].required_items:
                            if not i in self.inventory:
                                canEnterRoom = False
                else:
                    canEnterRoom = False

                if canEnterRoom and room is not self.previous_room:
                    room_choices.append(room)


            # The bot has nowhere to go but backwards, and hasn't accomplished anything in this room, dead run.
            if len(room_choices) == 0:
                if not hasPerformedAction:
                    reset = True
                else:
                    room_choices.append(self.previous_room)

            if len(room_choices) > 0:
                next_room = random.choice(room_choices)
                self.previous_room = self.current_room
                self.current_room = next_room

                # Once certain rooms have been 100%, remove them to reduce the chance of the bot running into dead ends
                if self.previous_room == "laboratory":
                    self.rooms.pop("laboratory")
                if self.previous_room == "observatory":
                    self.rooms.pop("observatory")
                if self.previous_room == "guest_room":
                    self.rooms.pop("guest_room")
                if self.previous_room == "clockworks":
                    self.rooms.pop("clockworks")
                if self.previous_room == "greenhouse":
                    self.rooms.pop("greenhouse")
                if self.previous_room == "bedroom":
                    self.rooms.pop("bedroom")
                if self.previous_room == "mouse_door":
                    self.rooms.pop("mouse_door")
                if self.previous_room == "fake_treasure_room":
                    self.rooms.pop("fake_treasure_room")

                # Change required_items of some rooms so they will only return once they have certain items
                if self.previous_room == "wine_cellar" and "doll_head" in self.inventory:
                    self.rooms["kitchen"].required_items = ["bottle_1", "bottle_2", "bottle_3"]
                if self.previous_room == "counts_room" and "lever" in self.inventory:
                    self.rooms["counts_room"].required_items = ["girl_ghost"]

                if self.previous_room == "library" and "nitro" in self.inventory:
                    self.rooms.pop("library")
                if self.previous_room == "tower_2" and "spring" in self.inventory:
                    self.rooms.pop("tower_2")
                if self.previous_room == "dining_room" and "dentures" in self.inventory:
                    self.rooms.pop("dining_room")
                if self.previous_room == "counts_room" and "bugle" in self.inventory:
                    self.rooms.pop("counts_room")
                if self.previous_room == "hunting_room" and "penny" in self.inventory:
                    self.rooms.pop("hunting_room")
                if self.previous_room == "skull_stairs" and "bottle_2" in self.inventory:
                    self.rooms.pop("skull_stairs")
                if "tower_1" in self.rooms and self.current_room != "tower_1" and "bottle_1" in self.inventory and "bottle_2" in self.inventory and "bottle_3" in self.inventory and "old_ghost" in self.inventory:
                    self.rooms.pop("tower_1")

                # Game Completion, write output walkthrough log
                if self.current_room == "finish":
                    output += (f"Finished game in {self.current_moves} moves\n")
                    if self.current_moves < self.best_win:
                        file = open(os.path.dirname(os.path.realpath(__file__)) + f"/{self.current_moves}.txt", "w")
                        file.write(output)
                        file.close()
                        self.best_win = self.current_moves
                    reset = True

                output += (f"[{self.current_room}]\n")
                self.current_moves += 1

                # If the bot takes too long, just end the run,
                if self.current_moves > self.max_moves:
                    reset = True

if __name__ == "__main__":
    skipper = Skipper()
    skipper.reset()
    skipper.loop()