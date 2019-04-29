class Point:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

class Room:
  def __init__(self, x: int , y: int, width: int, height: int):
    self.x = x
    self.y = y
    self.width = width
    self.height = height


  def center(self):
    return Point(x=(self.x + (self.width // 2)), y=(self.y + (self.height // 2)))


  def top_left(self):
    return Point(self.x, self.y)


  def bottom_right(self):
    return Point(self.x + self.width, self.y + self.height)

  def intersects(self, other_room):
    if(self.top_left().x > other_room.bottom_right().x or other_room.top_left().x > self.bottom_right().x):
      return False

    if(self.top_left().y > other_room.bottom_right().y or other_room.top_left().y > self.bottom_right().y):
      return False

    return True
