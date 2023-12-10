import pygame
import csv

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True


class Tri:
    def __init__(self, points, color=(255, 255, 255)):
        self.points = points #((x1, y1), (x2, y2), (x3, y3))
        self.color = color

    def draw(self, screen):
        pygame.gfxdraw.filled_polygon(screen, self.points, color)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
