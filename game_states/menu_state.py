import tcod
import tcod.event

class MenuState:
  def __init__(self, game, play_state):
    self.play_state = play_state
    self.game = game
    self.title = "PAUSED"

  def update(self):
    return None


  def render(self):
    self.game.root_console.clear()
    self.game.root_console.print(
      x=10,
      y=10,
      fg=tcod.white,
      string=self.title
    )
    tcod.console_flush()


  def handle_event(self, event):
    print("MenuState received event: ", event.type)
    if event.type == "KEYDOWN":
      print("MenuState received KEYDOWN event: ", event.sym)
      if event.sym == tcod.event.K_ESCAPE:
        print("MenuState received KEY_ESCAPE")
        # Pause the game
        self.switch_state(self.play_state)


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
