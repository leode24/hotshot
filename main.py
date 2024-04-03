import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame
from pygame.locals import QUIT
import math

# Define Game Variables
WIDTH, HEIGHT = 768, 432
BACKGROUND = (0, 0, 0)
ROTATION_SPEED = 2
SPEED = 0
score = 0
life = 3
CDS = False
rotation_angle = 0
y_pos = 313
x_pos = 90
cargo_y = 0
cargo_x = 0
color = (255, 255, 255)
screen_scroll = 0
bg_scroll = 0
rocket_blit = True
g_o = False
play = False

pygame.font.init()
pygame.mixer.init()
RS = pygame.mixer.Sound("rocket.mp3")
# BGmusic = pygame.mixer.Sound("BGmusic.mp3")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('HotShot')
clock = pygame.time.Clock()

game_over = pygame.image.load("game_over.png").convert_alpha()
restart = pygame.image.load("restart.png").convert_alpha()

bg = pygame.image.load("bg.png")

sprite1 = pygame.image.load("Rocket1.png").convert_alpha()
sprite2 = pygame.image.load("Rocket2.png").convert_alpha()
sprite3 = pygame.image.load("Rocket3.png").convert_alpha()
current_sprite = sprite3

# Load Terrain
terrain = pygame.image.load("terrain.png")

# Load 10x Targets
x10 = pygame.image.load("x10.png")

# Load 15x Targets
x15 = pygame.image.load("x15.png")

# Load 20x Targets
x20 = pygame.image.load("x20.png")

# Load 30x Targets
x30 = pygame.image.load("x30.png")

# Load Background Image
bg = pygame.image.load("bg.png")

# Load Cargo
cargo = pygame.image.load("ball.png").convert_alpha()

sprite_mask = pygame.mask.from_surface(sprite3)
terrain_mask = pygame.mask.from_surface(terrain)
x10_mask = pygame.mask.from_surface(x10)
x15_mask = pygame.mask.from_surface(x15)
x20_mask = pygame.mask.from_surface(x20)
x30_mask = pygame.mask.from_surface(x30)

bg_width = bg.get_width()
terrain_width = terrain.get_width()
x10_width = x10.get_width()
x15_width = x15.get_width()
x20_width = x20.get_width()
x30_width = x30.get_width()

bg_tiles = math.ceil(WIDTH / bg_width) + 2
terrain_tiles = math.ceil(WIDTH / terrain_width) + 2
x10_tiles = math.ceil(WIDTH / x10_width) + 2
x15_tiles = math.ceil(WIDTH / x15_width) + 2
x20_tiles = math.ceil(WIDTH / x20_width) + 2
x30_tiles = math.ceil(WIDTH / x30_width) + 2

velocity_x = 0
velocity_y = 0

cvelocity_x = 0
cvelocity_y = 0

font = pygame.font.SysFont('corbel', 35)

def find_slope(angle):
  slope = math.tan(math.radians(angle))
  return slope / 2

def resize_bg_image():
  global bg
  bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))

def resize_terrain_image():
  global terrain
  terrain = pygame.transform.scale(terrain, (screen.get_width(), screen.get_height()))

def kill(obj):
  del obj

# mask_image = cargo_mask.to_surface()

game_loop = True
while game_loop:
  clock.tick(30)
  screen.fill(BACKGROUND)
  cargo = pygame.transform.scale(cargo, (20, 20))
  game_over = pygame.transform.scale(game_over, (768, 432))
  restart = pygame.transform.scale(restart, (768, 241))

  screen_scroll -= velocity_x / 2
  bg_scroll -= velocity_x / 9

# Blit terrain, bg, and targets
  for i in range(0, bg_tiles):
    screen.blit(bg, (i * bg_width + bg_scroll - 4608, 0))
  for i in range(0, terrain_tiles):
    screen.blit(terrain, (i * terrain_width + screen_scroll - 4608, 0))
  for i in range(0, x10_tiles):
    screen.blit(x10, (i * x10_width + screen_scroll - 4608, 0))  
  for i in range(0, x15_tiles):
    screen.blit(x15, (i * x15_width + screen_scroll - 4608, 0))
  for i in range(0, x20_tiles):
    screen.blit(x20, (i * x20_width + screen_scroll - 4608, 0))
  for i in range(0, x30_tiles):
    screen.blit(x30, (i * x30_width + screen_scroll - 4608, 0))
  # screen.blit(mask_image, (x_pos + 161, y_pos - 59))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  if abs(bg_scroll) > bg_width:
    bg_scroll = 0

  if abs(screen_scroll) > terrain_width:
    screen_scroll = 0

  text1 = font.render(f'Lat. Speed: {round(velocity_x * (3 + 1/3))}', True, color)
  screen.blit(text1, (550, 10))
  text2 = font.render(f'Vert. Speed: {-round(velocity_y * (3 + 1/3))}', True, color)
  screen.blit(text2, (550, 45))
  text3 = font.render(f'Altitude: {-round((y_pos - 313) / 2.5)}', True, color)
  screen.blit(text3, (550, 80))
  text4 = font.render(f'Score: {score}', True, color)
  screen.blit(text4, (10, 10))
  text5 = font.render(f'Lives: {life}', True, color)
  screen.blit(text5, (10, 45))

  slope = find_slope(rotation_angle)

  if slope > 2:
    slope = 2
  elif slope < -2:
    slope = -2

  rotation_angle = rotation_angle % 360

  keys = pygame.key.get_pressed()

  if keys[pygame.K_UP] or keys[pygame.K_w]:
    if rotation_angle == 90:
      velocity_x -= 0.5 / 4
      velocity_y += 0
    elif rotation_angle == 270:
      velocity_x += 0.5 / 4
      velocity_y += 0
    elif rotation_angle > 90 and rotation_angle < 270:
      velocity_x += slope / 4
      velocity_y += 0.5 / 4
    else:
      velocity_x -= slope / 4
      velocity_y -= 0.5 / 4

  if play == True:
    RS.play()

  if play == False or g_o == True:
    RS.stop()

  if keys[pygame.K_UP] or keys[pygame.K_w]:
    play = True
    current_sprite = sprite2 if current_sprite == sprite1 else sprite1
  else:
    current_sprite = sprite3
    play = False

  if keys[pygame.K_SPACE] or keys[pygame.K_s] or keys[pygame.K_DOWN]:
    CDS = True    
  
  if CDS == True:
    x = cvelocity_x - velocity_x
    cargo_mask = pygame.mask.from_surface(cargo)
    screen.blit(cargo, (cargo_x + 228, cargo_y))
    cvelocity_y += 0.3
    cargo_x += x / 2

  if keys[pygame.K_p]:
    CDS = False
  
  if CDS == False:
    cvelocity_y = 0
    cvelocity_x = velocity_x
    cargo_y = y_pos
    cargo_x = x_pos

  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    rotation_angle += ROTATION_SPEED
    ROTATION_SPEED += 0.5 / 4

  elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    rotation_angle -= ROTATION_SPEED
    ROTATION_SPEED += 0.5 / 4

  else:
    ROTATION_SPEED = 1 / 4

  if keys[pygame.K_RSHIFT]:
    rotation_angle = 0

  if keys[pygame.K_m]:
    rotation_angle = 180
    velocity_x = 0

  if keys[pygame.K_ESCAPE] or keys[pygame.K_k]:
    game_loop = False

# set movement boundaries
  if velocity_y > 30:
    velocity_y = 30
  if velocity_y < -45:
    velocity_y = -45
  if velocity_x > 30:
    velocity_x = 30
  if velocity_x < -30:
    velocity_x = -30
  if ROTATION_SPEED > 10:
    ROTATION_SPEED = 10
  if slope > 1:
    slope = 1
  if rotation_angle < 1 and rotation_angle > 0:
    rotation_angle = 0
  if rotation_angle > 358 and rotation_angle < 0:
    rotation_angle = 0
  if life <= 0:
    g_o = True

  if g_o == True:  
    screen.blit(game_over, (0, -45))
    screen.blit(restart, (0, 241))
    rocket_blit = False
    velocity_y = -0.07
    velocity_x = 0
    rotation_speed = 0
    rotation_angle = 0
    screen_scroll = 0
    y_pos = 313
    life = 3
    score = 0
    if keys[pygame.K_RETURN]:
      g_o = False
      CDS = False
      rocket_blit = True

  rotated_sprite = pygame.transform.rotate(current_sprite, rotation_angle)
  rotated_sprite_rect = rotated_sprite.get_rect(center=(238, 18))

  velocity_y += 0.15 / 4
  rotated_sprite_rect.x += x_pos
  rotated_sprite_rect.y += y_pos

  rotated_sprite_mask = pygame.mask.from_surface(rotated_sprite)
  rotated_sprite_mask = sprite_mask

  if terrain_mask.overlap(sprite_mask, (x_pos + 161 - screen_scroll, y_pos - 59)) or terrain_mask.overlap(sprite_mask, (x_pos + 161 - screen_scroll + 4608, y_pos - 59)):
    velocity_y = -0.075
    velocity_x = 0
    rotation_speed = 0
  else:
    velocity_y += 0.15 / 4

  if (screen_scroll < -4463 and (screen_scroll <= 145 or screen_scroll >= -4462) and y_pos > 232) or ((screen_scroll <= -37 or screen_scroll >= 1) and terrain_mask.overlap(sprite_mask, (x_pos + 161 - screen_scroll, y_pos - 59)) or terrain_mask.overlap(sprite_mask, (x_pos + 161 - screen_scroll + 4608, y_pos - 59))):
    velocity_y = -0.07
    velocity_x = 0
    rotation_speed = 0
    rotation_angle = 0
    screen_scroll = 0
    y_pos = 313
    life -= 1
    if score < 15:
      score = 0
    else:
      score -= 15
      
  if CDS == True:  

    if terrain_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll, cargo_y)) or terrain_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll + 4608, cargo_y)) or terrain_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll - 4608, cargo_y)):
      CDS = False

    if x10_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll, cargo_y)) or x10_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll + 4608, cargo_y)):
      score += 10
      CDS = False


    if x15_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll, cargo_y)) or x15_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll + 4608, cargo_y)):
      score += 15
      CDS = False

    if x20_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll, cargo_y)) or x20_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll + 4608, cargo_y)):
      score += 20
      CDS = False

    if x30_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll, cargo_y)) or x30_mask.overlap(cargo_mask,(cargo_x + 228 - screen_scroll + 4608, cargo_y)):
      score += 30
      CDS = False

  y_pos += velocity_y

  cargo_y += cvelocity_y

  if rocket_blit == True:
    screen.blit(rotated_sprite, rotated_sprite_rect)

  pygame.display.update()