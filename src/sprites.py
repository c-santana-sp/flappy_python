import pygame
from settings import *

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
