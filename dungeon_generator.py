from map import Map
from room import Room
import tcod

class DungeonGenerator:
  def __init__(self, map_width, map_height, max_rooms, max_room_size, min_room_size):
    self.map_width = map_width
    self.map_height = map_height
    self.max_rooms = max_rooms
    self.max_room_size = max_room_size
    self.min_room_size = min_room_size

    self.map = Map(height=self.map_height, width=self.map_width)

  def generate(self):
    for r in range(self.max_rooms):
      new_room = self.generate_room()
      if not self.intersects_existing_room(new_room):
        self.add_room_to_map(new_room)
    return self.map


  def intersects_existing_room(self, new_room):
    # Check for intersections with existing rooms
    intersection = False
    for room in self.map.rooms:
      if new_room.intersects(room):
        intersection = True
        break
    return intersection


  def generate_room(self):
    # get a random width and height
    r_width = tcod.random_get_int(0, self.min_room_size, self.max_room_size)
    r_height = tcod.random_get_int(0, self.min_room_size, self.max_room_size)
    # get a random position on the map
    x = tcod.random_get_int(0, 0, self.map_width - r_width - 1)
    y = tcod.random_get_int(0, 0, self.map_height - r_height - 1)
    return Room(x=x, y=y, width=r_width, height=r_height)


  def add_room_to_map(self, new_room):
    # There are no intersections with existing rooms, so add the room to the map
    self.map.rooms.append(new_room)
    self.map.carve_room(new_room)

    if len(self.map.rooms) > 1:
      prev_room = self.map.rooms[len(self.map.rooms) - 2]
      self.connect_rooms(prev_room, new_room)


  def connect_rooms(self, room1, room2):
    # Randomly choose whether the tunnel goes horizontal or vertical first
    if tcod.random_get_int(0, 0, 1) == 1:
      self.map.create_horizontal_tunnel(room1.center().x, room2.center().x, room1.center().y)
      self.map.create_vertical_tunnel(room1.center().y, room2.center().y, room2.center().x)
    else:
      self.map.create_vertical_tunnel(room1.center().y, room2.center().y, room1.center().x)
      self.map.create_horizontal_tunnel(room1.center().x, room2.center().x, room2.center().y)
