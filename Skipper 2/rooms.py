class Room:
    def __init__(self, connected_rooms, required_items):   
        self.active = True
        self.connected_rooms = connected_rooms
        self.required_items = required_items
        
rooms = {
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