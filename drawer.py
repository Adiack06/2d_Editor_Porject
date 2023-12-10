import pygame
from pygame import gfxdraw
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
running = True


class Point:
    def __init__(self, center, radius=10):
        self.center = center  # (x, y)
        self.radius = radius

    def __getitem__(self, idx):
        if idx == 0:
            return self.center[0]  # x-coordinate
        elif idx == 1:
            return self.center[1]  # y-coordinate
        else:
            raise IndexError("Invalid index")
    def draw(self, screen, color):
        centerX = self.center[0]
        centerY = self.center[1]
        pygame.draw.circle(screen, color, (centerX, centerY), self.radius)
    def touching(self, collidee):
        centerX, centerY = self.center
        collideeX, collideeY = collidee
        if math.sqrt((collideeX - centerX) ** 2 + (collideeY - centerY) ** 2) <= self.radius:
            return True
        return False

class Triangle:
    def __init__(self, points, color = (255,255,255)):
        self.points = [Point(point) for point in points]
        self.color = color

    def draw(self, screen):
        vertices = (self.points[0].center, (self.points[1].center), (self.points[2].center)) #((x1,y1),(x2,y2),(x3,y3))
        pygame.gfxdraw.filled_polygon(screen, vertices, self.color)
        self.points[0].draw(screen, (100, 0, 0))
        self.points[1].draw(screen, (100, 0, 0))
        self.points[2].draw(screen, (100, 0, 0))


tris = []
mpoints = []
mouse3Down = False
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.KEYDOWN:

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpoints.append(Point(event.pos))
            print("point added")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse3Down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse3Down = False
        if mouse3Down:
            for tri in tris:
                for point in tri.points:
                    if point.touching(pygame.mouse.get_pos()) == True:
                        print("hi")
                        point.center = (event.pos)
            pass

    if len(mpoints) >= 3:
        tris.append(Triangle(mpoints))
        print("Triangle added")
        mpoints = []

    for point in mpoints:
        point.draw(screen,(255,0,0))
        if point.touching(pygame.mouse.get_pos()) == True:
            print("touched")
    for tri in tris:
        tri.draw(screen)

    # Rendering
    pygame.display.flip()

pygame.quit()
