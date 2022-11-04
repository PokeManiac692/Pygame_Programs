"""
Simple Pygame program for moving around the user's screen with user key input
"""
import pygame
import constants
from spritesheet_functions import SpriteSheet
 
class Player(pygame.sprite.Sprite):
    """ This class represents the sprite that the player controls. """
 
    # -- Methods
    def __init__(self, x, y):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # -- Attributes
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.walls = None
 
        # This holds all the images for the animated walk left/right or up/down
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []
 
        # What direction is the player facing?
        self.direction = "D"

        # Reference to character's Sprite Sheet
        sprite_sheet = SpriteSheet("images/character.png")
      
        # Load all the DOWN facing images into a list
        # get_image(Top Left X Coordinate, Top Left Y Coordinate, Width, Height)
        w = 16
        h = 32
        image = sprite_sheet.get_image(0, 0, w, h)
        # Add each image from sprite-sheet to appropriate directional list (double the size)
        image = pygame.transform.scale(image,(w*2,h*2))
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(16, 0, w, h)
        image = pygame.transform.scale(image,(w*2,h*2))
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(32, 0, w, h)
        image = pygame.transform.scale(image,(w*2,h*2))
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(48, 0, w, h)
        image = pygame.transform.scale(image,(w*2,h*2))
        self.walking_frames_d.append(image)

        # Load all the UP facing images into a list using a loop!
        # get_image(Top Left X Coordinate, Top Left Y Coordinate, Width, Height)
        playerX = 0
        playerY = 64
        for i in range(0,4):
          image = sprite_sheet.get_image(playerX, playerY, w, h)
          image = pygame.transform.scale(image,(w*2,h*2))
          self.walking_frames_u.append(image)
          playerX += 16
          
        # Load all the left/right facing images into a list using a loop
        playerX = 0
        playerY = 32
        for i in range(0,4):
          image = sprite_sheet.get_image(playerX, playerY, w, h)
          image = pygame.transform.scale(image,(w*2,h*2))
          self.walking_frames_r.append(image)
          # flip the image for left images
          image = pygame.transform.flip(image, True, False)
          image = pygame.transform.scale(image,(w*2,h*2))
          self.walking_frames_l.append(image)
          playerX += 16
 
        # Set the image the player starts with
        self.image = self.walking_frames_d[0]
 
        # Set a reference to the image rect.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    
    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x
        if self.direction == "R":
            frame = ((pos // 30) % len(self.walking_frames_r))
            self.image = self.walking_frames_r[frame]
        elif self.direction == "L":
            frame = ((pos // 30) % len(self.walking_frames_l))
            self.image = self.walking_frames_l[frame]
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise, if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
        pos2 = self.rect.y
        if self.direction == "U":
            frame = ((pos2 // 30) % len(self.walking_frames_u))
            self.image = self.walking_frames_u[frame]
        elif self.direction == "D":
            frame = ((pos2 // 30) % len(self.walking_frames_d))
            self.image = self.walking_frames_d[frame]
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        
        
 
 
class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

def draw_wall(x_pos, y_pos, width, height):
    """
    creates a wall object and adds it to the wall list
    """
    wall = Wall(x_pos, y_pos, width, height)
    wall_list.add(wall)
    all_sprite_list.add(wall)

# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create 800x600 sized screen using Constants file
screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
 
# Set the title of the window
pygame.display.set_caption('Test')
 
# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()
 
# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()

draw_wall(0, 0, 32, 720)    # long left side wall
draw_wall(10,0,790,10)      # top of screen wall
draw_wall(10, 200, 100, 10) # small wall from left side of wall
draw_wall(768, 0, 32, 720)  # long right side wall
# What happens if user keeps going downwards?

# Create the player paddle object
player = Player(50, 50)
player.walls = wall_list

all_sprite_list.add(player)

clock = pygame.time.Clock()
 
done = False

# Main Game Loop
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
                player.direction = "L"
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
                player.direction = "R"
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
                player.direction = "U"
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)
                player.direction = "D"
            elif event.key == pygame.K_ESCAPE:
                done = True
 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)
 
    all_sprite_list.update()
    screen.fill(constants.WHITE)
    all_sprite_list.draw(screen)

    pygame.display.flip()
 
    clock.tick(30)
 
pygame.quit()