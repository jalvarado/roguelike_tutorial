import tcod
import tcod.event
import settings
import colors
from .menu_state import MenuState

class PlayState:
  def __init__(self, game):
    self.game = game
    self.player = self.game.player
    self.fov_recompute = True


  def update(self):
    if self.fov_recompute:
      self.fov_recompute = False
      self.game.map.compute_fov(self.game.fov_map, self.player.x, self.player.y)
    for object in self.game.objects:
      object.map = self.game.map


  def render(self):
    for object in self.game.objects:
      object.draw(self.game.buffer)

    # Render the map to the console
    self.game.map.render(self.game.buffer, self.game.fov_map)

    # Blit the contents of the screen buffer
    self.game.buffer.blit(self.game.root_console, 0, 0, 0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

    tcod.console_flush()  # Show the console
    for object in self.game.objects:
      object.clear(self.game.buffer)


  def handle_event(self, event):
    print("PlayState received event: ", event.type)
    if event.type == "KEYDOWN":
      print("PlayState received KEYDOWN event: ", event.sym)
      if event.sym == tcod.event.K_ESCAPE:
        print("PLayState received KEY_ESCAPE")
        # Pause the game
        self.switch_state(MenuState(game=self.game, play_state=self))
      elif event.sym == tcod.event.K_LEFT:
        self.player.move(-1, 0)
        self.fov_recompute = True
      elif event.sym == tcod.event.K_RIGHT:
        self.player.move(1, 0)
        self.fov_recompute = True
      elif event.sym == tcod.event.K_UP:
        self.player.move(0, -1)
        self.fov_recompute = True
      elif event.sym == tcod.event.K_DOWN:
        self.player.move(0, 1)
        self.fov_recompute = True

  def switch_state(self, new_state):
    self.game.state.leave()
    self.game.state = new_state
    self.game.state.enter()


  def enter(self):
    print("Entering ", self.__class__.__name__)
    return None


  def leave(self):
    print("Leaving ", self.__class__.__name__)
    return None
