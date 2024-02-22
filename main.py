import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import sys
import pygame
from pygame.locals import QUIT
import random
import math

WIDTH, HEIGHT = 768, 432
BACKGROUND = (0, 0, 0)
ROTATION_SPEED = 1.8
SPEED = 0
score = 0
life = 0
CDS = False
pygame.font.init()
# pygame.mixer.init()
# RS = pygame.mixer.Sound("RocketEngine.wav")
# BGmusic = pygame.mixer.Sound("BGmusic.mp3")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('HotShot')
clock = pygame.time.Clock()

bg = pygame.image.load("bg.png")
cargo = pygame.image.load("Payload.png").convert_alpha()
sprite1 = pygame.image.load("Rocket1.png").convert_alpha()
sprite2 = pygame.image.load("Rocket2.png").convert_alpha()
sprite3 = pygame.image.load("Rocket3.png").convert_alpha()
current_sprite = sprite3

# Load Terrain
T1, T2, T3, T4, T5, T6 = [pygame.image.load(f"T{i}.png").convert_alpha() for i in range(1, 7)]

# T1 Targets
T1_10 = pygame.image.load("10T1.png").convert_alpha()
T1_15 = pygame.image.load("15T1.png").convert_alpha()
T1_20 = pygame.image.load("20T1.png").convert_alpha()

# T2 Targets
T2_10 = pygame.image.load("10T2.png").convert_alpha()
T2_15 = pygame.image.load("15T2.png").convert_alpha()
T2_20 = pygame.image.load("20T2.png").convert_alpha()
T2_30 = pygame.image.load("30T2.png").convert_alpha()

# T3 Targets
T3_10 = pygame.image.load("10T3.png").convert_alpha()
T3_15 = pygame.image.load("15T3.png").convert_alpha()
T3_20 = pygame.image.load("20T3.png").convert_alpha()
T3_30 = pygame.image.load("30T3.png").convert_alpha()

# T4 Targets
T4_10 = pygame.image.load("10T4.png").convert_alpha()
T4_15 = pygame.image.load("15T4.png").convert_alpha()

# T5 Targets
T5_10 = pygame.image.load("10T5.png").convert_alpha()
T5_15 = pygame.image.load("15T5.png").convert_alpha()
T5_20 = pygame.image.load("20T5.png").convert_alpha()

# T6 Targets
T6_10 = pygame.image.load("10T6.png").convert_alpha()
T6_15 = pygame.image.load("15T6.png").convert_alpha()
T6_20 = pygame.image.load("20T6.png").convert_alpha()
T6_30 = pygame.image.load("30T6.png").convert_alpha()

# camera_offset_x = WIDTH / 2
# camera_offset_y = HEIGHT / 2

sprite_mask = pygame.mask.from_surface(sprite3)
TM1 = pygame.mask.from_surface(T1)
TM2 = pygame.mask.from_surface(T2)
TM3 = pygame.mask.from_surface(T3)
TM4 = pygame.mask.from_surface(T4)
TM5 = pygame.mask.from_surface(T5)
TM6 = pygame.mask.from_surface(T6)
cargo_mask = pygame.mask.from_surface(cargo)


crotation = 0
rotation_angle = 0
y_pos = 313.8
x_pos = 90
color = (255, 255, 255)

velocity_x = SPEED * math.cos(math.radians(rotation_angle))
velocity_y = SPEED * math.sin(math.radians(rotation_angle))
cvelocity_x = 0
cvelocity_y = 0

font = pygame.font.SysFont('Corbel', 35)


def find_slope(angle):
  slope = math.tan(math.radians(angle))
  return slope / 2


def cargo_drop():
  global cvelocity_x, cvelocity_y, crotation, cargo_mask
  screen.blit(cargo, (x_pos + 200, y_pos))
  cargo_mask = pygame.mask.from_surface(cargo)
  cvelocity_x = SPEED * math.cos(math.radians(crotation))
  cvelocity_y = SPEED * math.sin(math.radians(crotation))


def resize_bg_image():
  global bg
  bg = pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))


def resize_T1_image():
  global T1
  T1 = pygame.transform.scale(T1, (screen.get_width(), screen.get_height()))


mask_image = sprite_mask.to_surface()

game_loop = True
while game_loop:
  clock.tick(18)
  screen.fill(BACKGROUND)
  # camera_x = x_pos - camera_offset_x
  # camera_y = y_pos - camera_offset_y
  cargo = pygame.transform.scale(cargo, (80, 80))
  # player_x = x_pos - camera_x
  # player_y = y_pos - camera_y
  #resize_bg_image()
  # resize_T1_image()
  #screen.blit(rotated_sprite, (player_x, player_y))

  screen.blit(bg, (0, 0))
  screen.blit(bg, (WIDTH, 0))
  screen.blit(T1, (0, 0))
  screen.blit(T2, (WIDTH, 0))
  screen.blit(T1_10, (0, 0))
  screen.blit(T1_15, (0, 0))
  screen.blit(T1_20, (0, 0))
  screen.blit(T2_10, (WIDTH, 0))
  screen.blit(T2_15, (WIDTH, 0))
  screen.blit(T2_20, (WIDTH, 0))
  screen.blit(T2_30, (WIDTH, 0))
  # screen.blit(mask_image, (x_pos + 161, y_pos - 59))
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()

  text1 = font.render(f'Lat. Speed: {round(velocity_x)}', True, color)
  screen.blit(text1, (550, 10))
  text2 = font.render(f'Vert. Speed: {-round(velocity_y)}', True, color)
  screen.blit(text2, (550, 45))
  text3 = font.render(f'Altitude: {-round(y_pos - 314)}', True, color)
  screen.blit(text3, (550, 80))
  text4 = font.render(f'Score: {score}', True, color)
  screen.blit(text4, (10, 10))

  slope = find_slope(rotation_angle)

  if slope > 2:
    slope = 2
  elif slope < -2:
    slope = -2

  rotation_angle = rotation_angle % 360
  
  keys = pygame.key.get_pressed()
  
  if keys[pygame.K_UP] or keys[pygame.K_w]:
    # RS.play()
    if rotation_angle == 90:
      velocity_x -= 0.5
      velocity_y += 0
    elif rotation_angle == 270:
      velocity_x += 0.5
      velocity_y += 0
    elif rotation_angle > 90 and rotation_angle < 270:
      velocity_x += slope
      velocity_y += 0.5
    else:
      velocity_x -= slope
      velocity_y -= 0.5


  if keys[pygame.K_UP] or keys[pygame.K_w ]:
    current_sprite = sprite2 if current_sprite == sprite1 else sprite1
  else:
    current_sprite = sprite3
    
    
  if keys[pygame.K_SPACE]:
      CDS = True    
  if CDS == True:
    cargo_drop()

  
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    rotation_angle += ROTATION_SPEED
    ROTATION_SPEED += 0.1
    
  elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    rotation_angle -= ROTATION_SPEED
    ROTATION_SPEED += 0.1
    
  else:
    ROTATION_SPEED = 1.8
    

  if keys[pygame.K_RETURN] or keys[pygame.K_RSHIFT]:
    velocity_y = -0.225
    velocity_x = 0
    rotation_angle = 0

  
  if keys[pygame.K_ESCAPE] or keys[pygame.K_k]:
    game_loop = False

  
  if velocity_y > 10:
    velocity_y = 10
  if ROTATION_SPEED > 30:
    ROTATION_SPEED = 30
  if slope > 1:
    slope = 1

  rotated_sprite = pygame.transform.rotate(current_sprite, rotation_angle)
  rotated_sprite_rect = rotated_sprite.get_rect(center=(238, 18))

  velocity_y += 0.15
  y_pos += velocity_y
  rotated_sprite_rect.x += x_pos
  rotated_sprite_rect.y += y_pos

  rotated_sprite_mask = pygame.mask.from_surface(rotated_sprite)
  rotated_sprite_mask = sprite_mask

  if TM1.overlap(sprite_mask, (x_pos + 161, y_pos - 59)):
    velocity_y = -0.075
    velocity_x = 0
    rotation_speed = 0
    # y_pos = y_pos - 70
    # rotation_angle = 0
    # score = score - 10
  else:
    velocity_y += 0.15

  if TM2.overlap(sprite_mask, (x_pos - 607, y_pos - 59)):
    velocity_y = -0.075
    velocity_x = 0
    rotation_speed = 0
    # if x_pos > 100 or x_pos < 10:
    #   y_pos = y_pos - 70
    # # rotation_angle = 0
    #   score = score - 10

  y_pos += velocity_y
  x_pos += velocity_x

  screen.blit(rotated_sprite, rotated_sprite_rect)

  pygame.display.update()
