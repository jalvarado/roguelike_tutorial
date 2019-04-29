import tcod
import tcod.event
import settings
from game_states import PlayState, MenuState
from game_object import GameObject
from dungeon_generator import DungeonGenerator

class Game:
  def __init__(self):
    self.root_console = None
    self.buffer = None
    self.objects = []
    self.state = None

    # Use a custom font
    tcod.console_set_custom_font(settings.FONT_PATH, settings.FONT_FLAGS)
    self.initialize_consoles()
    self.map = self.make_map()
    self.player = self.create_player()
    self.objects.append(self.player)

    # Initalize the FOV map
    self.fov_map = tcod.map_new(settings.MAP_WIDTH, settings.MAP_HEIGHT)
    for y in range(settings.MAP_HEIGHT):
      for x in range(settings.MAP_WIDTH):
        tcod.map_set_properties(
          self.fov_map,
          x,
          y,
          not self.map.tiles[x][y].block_sight,
          not self.map.tiles[x][y].blocked
        )

  def run(self):
    if self.state is None:
      print("No game state set.  Setting game state to PlayState")
      self.state = PlayState(self)
      self.state.enter()

    while True:
      self.state.update()
      self.state.render()

      for event in tcod.event.wait():
        if event.type == "QUIT":
          raise SystemExit()
        elif event.type == "KEYDOWN":
          print("Game received event: ", event.sym)
          self.state.handle_event(event)


  def create_player(self):
    # Create the initial players
    starting_room = self.map.rooms[tcod.random_get_int(0, 0, len(self.map.rooms) - 1)]
    return GameObject(x=starting_room.center().x, y=starting_room.center().y, char='@', color=tcod.white, map=self.map,
                      type='PLAYER')


  def initialize_consoles(self):
    window_title = 'Python 3 libtcod tutorial'
    fullscreen = False
    renderer = tcod.RENDERER_SDL2
    self.root_console = tcod.console_init_root(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, window_title, fullscreen,
                                               renderer)
    self.buffer = tcod.console.Console(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)
    tcod.sys_set_fps(settings.LIMIT_FPS)


  def make_map(self):
    return DungeonGenerator(
      map_width=settings.MAP_WIDTH,
      map_height=settings.MAP_HEIGHT,
      max_rooms=settings.MAX_ROOMS,
      max_room_size=10,
      min_room_size=5
    ).generate()
