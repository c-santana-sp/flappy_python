import pygame, sys, time
from settings import *
from sprites import BG, Ground, Obstacle, Player

class Game():
  def __init__(self):
    pygame.init()
    self.display_surface = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    pygame.display.set_caption('Flappy Python')
    self.clock = pygame.time.Clock()

    #sprite groups
    self.all_sprites = pygame.sprite.Group()
    self.collision_sprites = pygame.sprite.Group()

    #scale factor
    bg_height = pygame.image.load('../graphics/environment/background.png').get_height()
    self.scale = WINDOW_HEIGHT / bg_height

    #sprite setup
    BG(self.all_sprites, self.scale)
    Ground(self.all_sprites, self.scale)
    self.player = Player(self.all_sprites, self.scale / 1.5)

    #timer
    self.obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(self.obstacle_timer, OBSTACLE_SPAWN_TIMEOUT)

  def run(self):
    last_time = time.time()
    while True:
      #delta time
      dt = time.time() - last_time
      last_time = time.time()

      #event loop
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          self.player.jump()
        if event.type == self.obstacle_timer:
          Obstacle(self.all_sprites, self.scale * 1.1)

      #game logic
      self.display_surface.fill('black')
      self.all_sprites.update(dt)
      self.all_sprites.draw(self.display_surface)

      pygame.display.update()
      self.clock.tick(FPS)

if __name__ == '__main__':
  game = Game()
  game.run()