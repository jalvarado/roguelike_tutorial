from tile import Tile
import settings
import colors
import tcod

class Map:
  def __init__(self, height, width):
    self.height= height
    self.width = width

    self.tiles =  [
      [Tile(True) for y in range(settings.MAP_HEIGHT)]
      for x in range(settings.MAP_WIDTH)
    ]

    self.rooms = []


  def compute_fov(self, fov_map, x, y):
    tcod.map_compute_fov(
      fov_map,
      x,
      y,
      settings.TORCH_RADIUS,
      settings.FOV_LIGHT_WALLS,
      settings.FOV_ALGO
    )


  def render(self, buffer, fov_map):
    # Render the Map
    for y in range(settings.MAP_HEIGHT):
      for x in range(settings.MAP_WIDTH):
        visible = tcod.map_is_in_fov(fov_map, x, y)
        wall = self.tiles[x][y].block_sight
        if visible:
          self.tiles[x][y].explored = True
          if wall:
            tcod.console_set_char_background(buffer, x, y, colors.light_wall, tcod.BKGND_SET)
          else:
            tcod.console_set_char_background(buffer, x, y, colors.light_ground, tcod.BKGND_SET)
        else:
          if self.tiles[x][y].explored:
            if wall:
              tcod.console_set_char_background(buffer, x, y, colors.dark_wall, tcod.BKGND_SET)
            else:
              tcod.console_set_char_background(buffer, x, y, colors.dark_ground, tcod.BKGND_SET)



  def update(self, x, y, blocked, block_sight):
    self.tiles[x][y].blocked = blocked
    self.tiles[x][y].block_sight = block_sight


  def carve_room(self, room):
    for x in range(room.x+1, room.x + room.width):
      for y in range(room.y+1, room.y + room.height):
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False


  def create_room(self, x, y, height, width):
    for x1 in range(x+1, x+width):
      for y1 in range(y+1, y+height):
        self.tiles[x1][y1].blocked = False
        self.tiles[x1][y1].block_sight = False


  def create_horizontal_tunnel(self, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
      self.tiles[x][y].blocked = False
      self.tiles[x][y].block_sight = False


  def create_vertical_tunnel(self, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
      self.tiles[x][y].blocked = False
      self.tiles[x][y].block_sight = False
