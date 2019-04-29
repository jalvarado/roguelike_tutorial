import tcod

class GameObject:
  """
    This is a generic game object: the player, a monster, an item, the stairs...
    It's always represented by a character on the screen.
  """
  def __init__(self, x, y, char, color, map, type='NPC'):
    self.x = x
    self.y = y
    self.char = char
    self.color = color
    self.map = map
    self.type = type


  def move(self, dx, dy):
    if not self.map.tiles[self.x + dx][self.y + dy].blocked:
      self.x += dx
      self.y += dy


  def draw(self, console):
    # Set the color and then draw the character tha represents the object at its position
    console.print(x=self.x, y=self.y, fg=self.color, string=self.char)


  def clear(self, console):
    # Erase the character this object represents
    console.print(x=self.x, y=self.y, string=' ')

