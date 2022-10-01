import pygame
import random
import json

pygame.init()
pygame.font.init()

from pygame.locals import *
from sequencelist import *

window = pygame.display.set_mode((600, 600))

pygame.display.set_caption("Fishy Swim!")
clock = pygame.time.Clock()

white = (255, 255, 255)
gray = (150, 150, 150)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gamespeed = 5
score = 0
gamescreen = "title"

# Asset loading
scorefont = pygame.font.SysFont("Arial", 24)
largefont = pygame.font.SysFont("Arial", 84)
medfont = pygame.font.SysFont("Arial", 36)
background = pygame.image.load("assets/Background.png")
border = pygame.image.load("assets/border2.png")
coral = pygame.image.load("assets/coral.png")
borderblack = pygame.image.load("assets/borderblack.png")
logo = pygame.image.load("assets/logo.png")

jelly1 = pygame.image.load("assets/jelly1.png")
jelly1 = pygame.transform.scale(jelly1, (50, 50))
jelly2 = pygame.image.load("assets/jelly2.png")
jelly2 = pygame.transform.scale(jelly2, (50, 50))
jellydead1 = pygame.image.load("assets/jellydead1.png")
jellydead1 = pygame.transform.scale(jellydead1, (50, 50))
jellydead2 = pygame.image.load("assets/jellydead2.png")
jellydead2 = pygame.transform.scale(jellydead2, (50, 50))

crate = pygame.image.load("assets/crate.png")
crate = pygame.transform.scale(crate, (70, 70))
whaleR = pygame.image.load("assets/whaleR.png")
whaleR = pygame.transform.scale(whaleR, (220, 70))
whaleL = pygame.image.load("assets/whaleL.png")
whaleL = pygame.transform.scale(whaleL, (220, 70))
greenfish = pygame.image.load("assets/greenfish.png")
greenfish = pygame.transform.scale(greenfish, (70, 70))
redfish = pygame.image.load("assets/redfish.png")
redfish = pygame.transform.scale(redfish, (70, 70))
purplefishL = pygame.image.load("assets/purplefishL.png")
purplefishL = pygame.transform.scale(purplefishL, (70, 70))
purplefishR = pygame.image.load("assets/purplefishR.png")
purplefishR = pygame.transform.scale(purplefishR, (70, 70))
yellowfishL = pygame.image.load("assets/yellowfishL.png")
yellowfishL = pygame.transform.scale(yellowfishL, (70, 70))
yellowfishR = pygame.image.load("assets/yellowfishR.png")
yellowfishR = pygame.transform.scale(yellowfishR, (70, 70))

with open('usersave.json') as file:
  savedata = json.load(file)

# Class definitions

class Player:
  def __init__(self, column):
    self.color = red
    self.column = column
    self.x = 150 + ((self.column - 1) * 150) - 25
    self.y = 600
    self.rect = Rect(self.x, self.y, 50, 50)
    self.movingLeft, self.movingRight = False, False

  # Loads the images for the Player object
  def load_sprites(self):
    self.img1 = jelly1
    self.img2 = jelly2
    self.img3 = jellydead1
    self.img4 = jellydead2
    self.img = self.img1

  # What the Player should do when they die
  def die(self):
    global gamescreen
    gamescreen = "death"
    with open('usersave.json', 'w') as file:
      json.dump(savedata, file, indent=4)

  # Simple code to run every frame
  def update(self):
    global gamescreen
    self.rect = Rect(self.x, self.y, 50, 50)
    if gamescreen == "playing":
      if self.movingLeft:
        if self.x == 150 + ((self.column - 1) * 150) - 25:
          self.movingLeft = False
        else:
          self.x -= 25
      elif self.movingRight:
        if self.x == 150 + ((self.column - 1) * 150) - 25:
          self.movingRight = False
        else:
          self.x += 25
    if gamescreen == "starting" and self.y != 500:
      self.y -= 1
    for obs in obstacles:
      if self.rect.colliderect(obs.rect):
        self.color = green
        self.die()
      if obs.type == 3:
        if self.rect.colliderect(obs.rect2):
          self.color = green
          self.die()

  # Moves the player left
  def moveleft(self):
    self.column -= 1
    self.movingLeft = True

  # Moves the player right
  def moveright(self):
    self.column += 1
    self.movingRight = True

  # Displays the player on the screen
  def render(self):
    #pygame.draw.rect(window, self.color, self.rect)
    if gamescreen == "playing" or gamescreen == "death" or gamescreen == "starting":
      window.blit(self.img, (self.rect.left, self.rect.top))

class Obstacle:
  def __init__(self, column, type):
    self.column = column
    self.type = type
    if self.type == 1 or self.type == 3:
      self.width, self.height = 70, 70
    if self.type == 2:
      self.width, self.height = 220, 70
    if self.type == 4 or self.type == 5 or self.type == 6 or self.type == 7:
      self.width, self.height, self.x = 70, 70, 150 + ((self.column - 1) * 150) - 35
    if self.type == 6:
      self.direction = -1
    elif self.type == 7:
      self.direction = 1
    self.y = -100
    self.spawned = False

  # Loads the images for the obstacle object
  def load_sprites(self):
    if self.type == 1 or self.type == 3:
      self.img = crate
    elif self.type == 2:
      if self.column == 1:
        self.img = whaleR
      else:
        self.img = whaleL
    elif self.type == 4:
      self.img = greenfish
    elif self.type == 5:
      self.img = redfish
    elif self.type == 6:
      self.img1 = purplefishL
      self.img2 = purplefishR
      self.img = self.img1
    elif self.type == 7:
      self.img1 = yellowfishL
      self.img2 = yellowfishR
      self.img = self.img2

  # Code to run every frame
  def update(self):
    if gamescreen == "playing":
      self.y += gamespeed
    if self.type == 1 or self.type == 2:
      self.rect = Rect(150 + ((self.column - 1) * 150) - 35, self.y, self.width, self.height) # 35 is half the width
    elif self.type == 3:
      self.rect = Rect(150 + ((0) * 150) - 35, self.y, self.width, self.height)
      self.rect2 = Rect(150 + ((2) * 150) - 35, self.y, self.width, self.height)
    elif self.type == 4:
      self.rect = Rect(self.x, self.y, self.width, self.height)
      if gamescreen == "playing":
        self.x -= 5
      if self.x <= -70:
        self.x = 600
    elif self.type == 5:
      self.rect = Rect(self.x, self.y, self.width, self.height)
      if gamescreen == "playing":
        self.x += 5
      if self.x >= 600:
        self.x = -70
    elif self.type == 6 or self.type == 7:
      self.rect = Rect(self.x, self.y, self.width, self.height)
      if gamescreen == "playing":
        self.x += 5 * self.direction
      if self.x <= 75 or self.x >= 455:
        self.direction = -self.direction
      if self.direction < 0:
        self.img = self.img1
      else:
        self.img = self.img2

  # Display the obstacle on screen
  def render(self):
    #pygame.draw.rect(window, gray, self.rect)
    window.blit(self.img, (self.rect.left, self.rect.top))
    if self.type == 3:
      window.blit(self.img, (self.rect2.left, self.rect2.top))

# Variable declarations

player = Player(2)
player.load_sprites()
obstacles = []
bordery = 0
coraly = 0
newHS = False
parallax = savedata["backgrounds"]

# Function definitions

# Creates a new obstacle
def new_obstacle(column, type):
  obstacles.append(Obstacle(column, type))
  obstacles[len(obstacles) - 1].load_sprites()

generation = []

for seq in random.choice(sequences):
  generation.append(seq)

# Spawns an obstacle from a sequence
def spawn_obstacle():
  global generation
  global sequences
  new_obstacle(generation[0][1], generation[0][0])
  generation.pop(0)

# Updates the rainbow color every frame
RBred, RBgreen, RBblue = 255, 0, 0
rainbowphase = "greenUP"
def rainbow_update():
  global rainbow
  global rainbowphase
  global RBred
  global RBgreen
  global RBblue
  if rainbowphase == "greenUP":
    RBgreen += 2.5
    if RBgreen == 255:
      rainbowphase = "redDOWN"
  elif rainbowphase == "redDOWN":
    RBred -= 2.5
    if RBred == 0:
      rainbowphase = "blueUP"
  elif rainbowphase == "blueUP":
    RBblue += 2.5
    if RBblue == 255:
      rainbowphase = "greenDOWN"
  elif rainbowphase == "greenDOWN":
    RBgreen -= 2.5
    if RBgreen == 0:
      rainbowphase = "redUP"
  elif rainbowphase == "redUP":
    RBred += 2.5
    if RBred == 255:
      rainbowphase = "blueDOWN"
  elif rainbowphase == "blueDOWN":
    RBblue -= 2.5
    if RBblue == 0:
      rainbowphase = "greenUP"

# Gameloop, runs infinitely

frame = 0
gameLoop = True
while gameLoop:
  window.fill(white)
  window.blit(background, (0, 0))

  if gamescreen == "deathscreen":
    rainbow_update()

  if gamescreen == "playing" or gamescreen == "title" or gamescreen == "starting":
    coraly = (coraly + gamespeed / 5) % 600
  if parallax:
    window.blit(coral, (0, coraly))
    window.blit(coral, (0, coraly - 600))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      gameLoop = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT and gamescreen == "playing":
        if player.column > 1 and not player.movingLeft and not player.movingRight:
          player.moveleft()
      elif event.key == pygame.K_RIGHT and gamescreen == "playing":
        if player.column < 3 and not player.movingRight and not player.movingLeft:
          player.moveright()
      elif event.key == pygame.K_SPACE:
        if gamescreen == "deathscreen":
          obstacles.clear()
          score = 0
          player.y = 500
          player.column = 2
          player.x = 275
          player.img = player.img1
          newHS = False
          for seq in random.choice(sequences):
            generation.append(seq)
          gamescreen = "playing"
        elif gamescreen == "title":
          gamescreen = "starting"
      elif event.key == pygame.K_b and gamescreen == "playing":
        parallax = not parallax
        savedata["backgrounds"] = parallax
      elif event.key == pygame.K_m and gamescreen == "deathscreen":
        obstacles.clear()
        score = 0
        player.y = 600
        player.column = 2
        player.x = 275
        player.img = player.img1
        newHS = False
        gamescreen = "title"

  player.update()
  player.render()

  if frame % 10 == 0 and frame != 0 and gamescreen == "playing":
    score += 1
    if score > savedata["highscore"]:
      savedata["highscore"] = score
      newHS = True

  if frame % 5 == 0 and (gamescreen == "playing" or gamescreen == "starting"):
    if player.img == player.img1:
      player.img = player.img2
    else:
      player.img = player.img1

  if gamescreen == "death":
    if frame % 10 == 0:
      if player.img == player.img3:
        player.img = player.img4
      else:
        player.img = player.img3
    player.y += 1
    if player.y > 600:
      gamescreen = "deathscreen"
      fade = 0

  gamespeed = (7500 / ((-score * 0.5) - 375)) + 25

  if len(obstacles) == 0 and gamescreen == "playing":
    spawn_obstacle()

  for obs in obstacles:
    obs.update()
    if obs.y >= 300 and obs.spawned == False:
      if len(generation) != 0:
        spawn_obstacle()
      else:
        for seq in random.choice(sequences):
          generation.append(seq)
        spawn_obstacle()
      obs.spawned = True
    obs.render()

  if len(obstacles) > 0:
    if obstacles[0].y > 600:
      obstacles.pop(0)

  if gamescreen != "title" and gamescreen != "starting":
    scoretext = scorefont.render(f'Score: {score}', False, black)
    window.blit(scoretext, (25, 15))
    scoretext = scorefont.render(f'Highscore: {savedata["highscore"]}', False, black)
    window.blit(scoretext, (25, 54))

  if gamescreen == "title" or gamescreen == "starting":
    if gamescreen == "starting":
      scrolly += gamespeed
    else:
      scrolly = 0
    window.blit(logo, (150, 50 + scrolly))
    playtext = medfont.render(f'Press SPACE to play!', False, black)
    playrect = playtext.get_rect(center=(300, 480 + scrolly))
    window.blit(playtext, playrect)
    if scrolly + 50 >= 600:
      gamescreen = "playing"

  if gamescreen == "deathscreen":
    fadescreen = pygame.Surface((600, 600))
    fadescreen.set_alpha(fade)
    if newHS:
      fadescreen.fill((RBred, RBgreen, RBblue))
    else:
      fadescreen.fill(blue)
    window.blit(fadescreen, (0, 0))
    if fade < 255:
      fade += 5
    else:
      youlost = largefont.render("You Lost!", False, white)
      ylrect = youlost.get_rect(center=(300, 150))
      window.blit(youlost, ylrect)
      finalscore = scorefont.render(f'Your final score was: {score}', False, white)
      fsrect = finalscore.get_rect(center=(300, 220))
      window.blit(finalscore, fsrect)
      if newHS:
        newHStext = scorefont.render("NEW HIGHSCORE!!!", False, white)
        nhsrect = newHStext.get_rect(center=(300, 260))
        window.blit(newHStext, nhsrect)
      restarttext = scorefont.render(f'Press SPACE to restart', False, white)
      rtrect = restarttext.get_rect(center=(300, 480))
      window.blit(restarttext, rtrect)
      menutext = scorefont.render(f'Press M to go to the main menu', False, white)
      mtrect = menutext.get_rect(center=(300, 530))
      window.blit(menutext, mtrect)

  if gamescreen == "playing" or gamescreen == "title" or gamescreen == "starting":
    bordery = (bordery + gamespeed) % 600
  window.blit(border, (0, bordery))
  window.blit(border, (0, bordery - 600))

  if gamescreen == "deathscreen":
    borderblack.set_alpha(fade)
    window.blit(borderblack, (0, bordery))
    window.blit(borderblack, (0, bordery - 600))

  frame += 1
  pygame.display.flip()
  clock.tick(60)

pygame.quit()