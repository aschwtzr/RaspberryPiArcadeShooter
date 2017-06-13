from sense_hat import SenseHat
from time import sleep
from random import randint

#set up Sense HAT: create instance, clear previous game and set low light
sense = SenseHat()
sense.clear()
sense.low_light = True

#global variables
alive = True
bullets = []
baddies = []
timer = 0
score = 0
threshold = 8

class Player(object):
  def __init__(self,x,y):
    self.color = (0,252,0)
    sense.set_pixel(x,y,self.color)
    self.x = x
    self.y = y

   #lastMove tracks players's direction for firing bullets
    self.lastMove = ""

  def move(self, direction):
      #update player's direction and calculate new x, y variables
      self.lastMove = direction
      x, y = getCoordinates(self.x, self.y, direction)

      #check that new x, y variables are inside LED grid
      if -1 < x < 8 and -1 < y < 8:
        sense.set_pixel(self.x,self.y,0,0,0)
        self.x, self.y = x, y
        sense.set_pixel(self.x,self.y,self.color)

  def fire(self):
    x, y = getCoordinates(self.x, self.y, self.lastMove)
    if -1 < x < 8 and -1 < y < 8:
      bullet = Bullet(x,y,self.lastMove)
      bullets.append(bullet)

class Bullet(object):
  def __init__(self,x,y,direction):
    self.color = (255,69,0)
    self.x, self.y, self.direction = x, y, direction

    sense.set_pixel(x,y, self.color)

class Baddie(object):
  def __init__(self,x,y):
    self.color = (165,42,42)
    self.x, self.y = x, y
    self.direction = ""
    sense.set_pixel(x,y,self.color)

  def getDirection(self):
    integer = randint(1,4)
    if integer == 1:
      self.direction = "up"
    elif integer == 2:
      self.direction = "down"
    elif integer == 3:
      self.direction = "left"
    elif integer == 4:
      self.direction = "right"

#function returns new x, y coordinates
def getCoordinates(x,y,direction):
  if direction == "up":
    y -= 1
  elif direction == "down":
    y += 1
  elif direction == "left":
    x -= 1
  elif direction == "right":
    x += 1
  return (x,y)

def moveObjects():
  for baddie in baddies:
    x, y = getCoordinates(baddie.x,baddie.y,baddie.direction)

    #check that new location is valid, else give Baddie new direction
    if -1 < x < 8 and -1 < y < 8:
      obj = sense.get_pixel(x,y)

      #check if player is at new position
      if obj == [0,252,0]:
        global alive
        alive = False

      #check if bullet is at new position
      elif obj == [248,68,0]:
        sense.set_pixel(baddie.x,baddie.y,0,0,0)
        del baddies[baddies.index(baddie)]
        global score
        score += 1
        break

      #move baddie object
      else:
        sense.set_pixel(baddie.x,baddie.y,0,0,0)
        baddie.x, baddie.y = x, y
        sense.set_pixel(x,y,baddie.color)
    else:
      baddie.getDirection()
  #moving baddies will go here.

  for bullet in bullets:
    x, y = getCoordinates(bullet.x,bullet.y,bullet.direction)
    if -1 < x < 8 and -1 < y < 8:
      sense.set_pixel(bullet.x,bullet.y,0,0,0)
      bullet.x, bullet.y = x, y
      sense.set_pixel(x,y,bullet.color)
    else:
      sense.set_pixel(bullet.x,bullet.y,0,0,0)
      del bullets[bullets.index(bullet)]

player = Player(0,0)

while True:
  sleep(1)

  #handles joystick events coming from player
  for event in sense.stick.get_events():
    if event.direction != "middle":
      player.move(event.direction)

    else:
      player.fire()

  moveObjects()

  #resets player pixel in case it's overridden by Bullet objects
  sense.set_pixel(player.x,player.y, player.color)

  #threshold and timer logic for creating new Baddies
  timer += 1
  if timer > threshold:
    timer = 0
    baddie = Baddie(randint(0,7),randint(0,7))
    baddie.getDirection()
    baddies.append(baddie)

    #score and threshold go here
  if score > 10:
    threshold = 6

  elif score > 15:
    threshold = 4

  if not alive:
    break

sense.show_message("REKT... SCORE = " + str(score), text_colour=[255, 0, 0])
