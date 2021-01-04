class Item:
    def __init__(self, room, required_items):  
        self.room = room
        self.required_items = required_items
        self.active = True

items = {
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