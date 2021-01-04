import random
from datetime import datetime
import os
from rooms import rooms
from items import items

class Skipper (object):
    def __init__(self):
        self.inventory = []
        self.current_room = "main_hall"
        self.previous_room = "null"
        self.current_moves = 0
        self.longest_run = 0
        self.startTime = datetime.now()
        self.best_win = 999
        self.max_moves = 80
        self.total_attempts = 0
    
    def reset (self):
        os.system('cls')
        print("SKIPPER AND SKEETO 2 SOLVER")
        print("===========================")
        print(f"Elapsed Time: {datetime.now() - self.startTime}")
        print(f"Total Attempts: {self.total_attempts}")
        print(f"Longest Run: {self.longest_run}")
        print(f"Best Win (Least Moves): {self.best_win}")
        rooms["kitchen"].required_items = None
        rooms["counts_room"].required_items = None
        for key, value in items.items():
            value.active = True
        for key, value in rooms.items():
            value.active = True
        self.current_moves = 0
        self.current_room = "main_hall"
        self.previous_room = "null"
        self.inventory = []
        self.total_attempts += 1

    def loop (self):
        output = ""
        reset = False
        while True:
            if reset:
                output = ""
                reset = False
                self.reset()
            room_choices = []
            hasPerformedAction = False

            # Gather all possible collectable items in the room
            for key, value in items.items():
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
            for room in rooms[self.current_room].connected_rooms:
                canEnterRoom = True
                if rooms[room].active:
                    if rooms[room].required_items is not None:
                        for i in rooms[room].required_items:
                            if not i in self.inventory:
                                canEnterRoom = False
                else:
                   canEnterRoom = False 

                if canEnterRoom and room is not self.previous_room:
                    room_choices.append(room)

            # The bot has nowhere to go but backwards, and hasn't accomplished anything in this room, dead run.
            if len(room_choices) == 0:
                if not hasPerformedAction:
                    if self.current_moves > self.longest_run:
                        self.longest_run = self.current_moves
                    reset = True
                else:
                    room_choices.append(self.previous_room)
                    
            if len(room_choices) > 0:
                next_room = random.choice(room_choices)
                self.previous_room = self.current_room
                self.current_room = next_room

                # Once certain rooms have been 100%, remove them to reduce the chance of the bot running into dead ends
                if self.previous_room == "laboratory":
                    rooms["laboratory"].active = False
                if self.previous_room == "observatory":
                    rooms["observatory"].active = False
                if self.previous_room == "guest_room":
                    rooms["guest_room"].active = False
                if self.previous_room == "clockworks":
                    rooms["clockworks"].active = False
                if self.previous_room == "greenhouse":
                    rooms["greenhouse"].active = False
                if self.previous_room == "bedroom":
                    rooms["bedroom"].active = False
                if self.previous_room == "mouse_door":
                    rooms["mouse_door"].active = False
                if self.previous_room == "fake_treasure_room":
                    rooms["fake_treasure_room"].active = False

                # Change required_items of some rooms so they will only return once they have certain items
                if self.previous_room == "wine_cellar" and "doll_head" in self.inventory:
                    rooms["kitchen"].required_items = ["bottle_1", "bottle_2", "bottle_3"]
                if self.previous_room == "counts_room" and "lever" in self.inventory:
                    rooms["counts_room"].required_items = ["girl_ghost"]

                if self.previous_room == "library" and "nitro" in self.inventory:
                    rooms["library"].active = False
                if self.previous_room == "tower_2" and "spring" in self.inventory:
                    rooms["tower_2"].active = False
                if self.previous_room == "dining_room" and "dentures" in self.inventory:
                    rooms["dining_room"].active = False
                if self.previous_room == "counts_room" and "bugle" in self.inventory:
                    rooms["counts_room"].active = False
                if self.previous_room == "hunting_room" and "penny" in self.inventory:
                    rooms["hunting_room"].active = False
                if self.previous_room == "skull_stairs" and "bottle_2" in self.inventory:
                    rooms["skull_stairs"].active = False
                if self.current_room != "tower_1" and "bottle_1" in self.inventory and "bottle_2" in self.inventory and "bottle_3" in self.inventory and "old_ghost" in self.inventory:
                    rooms["tower_1"].active = False

                # Game Completion, write output walkthrough log
                if self.current_room == "finish":
                    output += (f"[Finish]\nFinished game in {self.current_moves+1} moves\n")
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