import pygame
from settings import *
from random import choice, randint

class BG(pygame.sprite.Sprite):
  def __init__(self, groups, scale):
    super().__init__(groups)
    bg_img = pygame.image.load('../graphics/environment/background.png').convert()

    full_height = bg_img.get_height() * scale
    full_width = bg_img.get_width() * scale
    full_sized_img = pygame.transform.scale(bg_img, (full_width, full_height)) 

    self.image = pygame.Surface((full_width * 2, full_height))
    self.image.blit(full_sized_img, (0, 0))
    self.image.blit(full_sized_img, (full_width, 0))

    self.rect = self.image.get_rect(topleft = (0, 0))
    self.position = pygame.math.Vector2(self.rect.topleft)

  def update(self, dt):
    self.position.x -= BACKGROUND_VEL * dt

    if self.rect.centerx <= 0:
      self.position.x = 0

    self.rect.x = round(self.position.x)

class Ground(pygame.sprite.Sprite):
  def __init__(self, groups, scale):
    super().__init__(groups)

    #image
    ground_surface = pygame.image.load('../graphics/environment/ground.png').convert_alpha()
    self.image = pygame.transform.scale(ground_surface, pygame.math.Vector2(ground_surface.get_size()) * scale)

    #position
    self.rect = self.image.get_rect(bottomleft = (0, WINDOW_HEIGHT))
    self.position = pygame.math.Vector2(self.rect.bottomleft)

    #mask
    self.mask = pygame.mask.from_surface(self.image)

  def update(self, dt):
    self.position.x -= GROUND_VEL * dt

    if self.rect.centerx <= 0:
      self.position.x = 0

    self.rect.x = round(self.position.x)

class Player(pygame.sprite.Sprite):
  def __init__(self, groups, scale):
    super().__init__(groups)

    #image
    self.import_frames(scale)
    self.frame_index = 0
    self.image = self.frames[self.frame_index]

    #rect
    self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
    self.position = pygame.math.Vector2(self.rect.topleft)

    #movement
    self.gravity = GRAVITY_VEL
    self.direction = 0

    #mask
    self.mask = pygame.mask.from_surface(self.image)

  def import_frames(self, scale):
    self.frames = []

    for i in range(3):
      # print(i)
      current_img = pygame.image.load(f'../graphics/plane/red{i}.png').convert_alpha()
      img = pygame.transform.scale(current_img, pygame.math.Vector2(current_img.get_size()) * scale)
      self.frames.append(img)

  def update(self, dt):
    self.apply_gravity(dt)
    self.animate(dt)
    self.rotate()

  def apply_gravity(self, dt):
    self.direction += self.gravity * dt
    self.position.y += self.direction * dt
    self.rect.y = round(self.position.y)

  def jump(self):
    self.direction = JUMP_VEL

  def animate(self, dt):
    self.frame_index += PLAYER_ANIMATION_SPEED * dt
    if self.frame_index >= len(self.frames):
      self.frame_index = 0
    self.image = self.frames[int(self.frame_index)]

    self.mask = pygame.mask.from_surface(self.image)

  def rotate(self):
    rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * PLAYER_ROTATION_SPEED, 1)
    self.image = rotated_plane

    self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
  def __init__(self, groups, scale):
    super().__init__(groups)
    
    orientation = choice(('up', 'down'))
    surf = pygame.image.load(f'../graphics/obstacles/{choice((0, 1))}.png').convert_alpha()

    self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scale)

    x = WINDOW_WIDTH + randint(40, 100)

    if orientation == 'up':
      y = WINDOW_HEIGHT + randint(10, 50)
      self.rect = self.image.get_rect(midbottom = (x, y))
    else:
      y = randint(-50, -10)
      self.image = pygame.transform.flip(self.image, False, True)
      self.rect = self.image.get_rect(midtop = (x, y))

    #position
    self.position = pygame.math.Vector2(self.rect.topleft)

    #mask
    self.mask = pygame.mask.from_surface(self.image)

  def update(self, dt):
    self.position.x -= OBSTACLE_VEL * dt
    self.rect.x = round(self.position.x)
    
    if self.rect.right <= -self.image.get_width() + 10:
      self.kill()
