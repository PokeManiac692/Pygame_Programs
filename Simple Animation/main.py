import pygame
'''
Create a class that will represent a player object!
this class will inherit the Sprite functions in the pygame library
'''


class Player(pygame.sprite.Sprite):
  def __init__(self, pos_x, pos_y):
    """
    Function to initialize/create a player object
    (parameters are the x,y coordinates of the player)
    """
    super().__init__()
    self.walk_animation = False
    self.sprites = []
    # Load each individual walking frame into the list
    self.sprites.append(pygame.image.load('images/forward1.png'))
    self.sprites.append(pygame.image.load('images/forward2.png'))
    self.sprites.append(pygame.image.load('images/forward3.png'))
    self.sprites.append(pygame.image.load('images/forward4.png'))
    self.current_sprite = 0
    self.image = self.sprites[self.current_sprite]

    self.rect = self.image.get_rect()
    self.rect.topleft = [pos_x,pos_y]

  def walk(self):
    self.walk_animation = True
  
  def update(self,speed):
    if self.walk_animation == True:
      self.current_sprite += speed
    if int(self.current_sprite) >= len(self.sprites):
      self.current_sprite = 0

    self.image = self.sprites[int(self.current_sprite)]

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

# Get screen info
width = screen.get_width()
height = screen.get_height()

# Define a font
font1 = pygame.font.SysFont('Arial', 14)

# Render some text
text = font1.render("Press \"s\" key to animate!", True, (255,255,255))

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player(160,100)
moving_sprites.add(player)

# Main Game Loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_s:
        player.walk()
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_s:
        player.walk_animation = False
        player.current_sprite = 0

	# Drawing
  screen.fill((0,0,0))
  moving_sprites.draw(screen)
  moving_sprites.update(0.25)
  # 400 pixel screen, offset 12pt font-84
  screen.blit(text, (((width/2)-84),((height/2)+100)))
  pygame.display.flip()
  clock.tick(30)

pygame.quit()