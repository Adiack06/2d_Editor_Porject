import pygame
from pygame import gfxdraw
import math
import csv

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
class ColorsSelector:
    def __init__(self, color , value,location):
        self.color = color
        self.value = value
        self.location = location

class Polygon:
    def __init__(self, points, color):
        self.points = [Point(point) for point in points]
        self.color = color

    def draw(self, screen):
        vertices = tuple(point.center for point in self.points) #((x1,y1),(x2,y2),(x3,y3))
        pygame.gfxdraw.filled_polygon(screen, vertices, self.color)
        for point in self.points:
            point.draw(screen, (100, 0, 0))
    def csvexport(self):
        x1,y1,x2,y2,x3,y3= (self.points[0].center[0],self.points[0].center[1],self.points[1].center[0],self.points[1].center[1],self.points[2].center[0],self.points[2].center[1],)  # ((x1,y1),(x2,y2),(x3,y3))
        r,g,b = self.color
        return(x1,y1,x2,y2,x3,y3,r,g,b)
    def csvimport(entry):
        x1, y1, x2, y2, x3, y3, r, g, b = map(int, entry)
        tripoints = [
            Point((x1, y1)),
            Point((x2, y2)),
            Point((x3, y3))
        ]
        polys.append(Polygon(tripoints, (r, g, b)))

polys = []
mpoints = []
mouse3Down = False
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_i:
                with open("map.csv", 'r', newline='') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    next(csv_reader)
                    for row in csv_reader:
                        Polygon.csvimport(row)
            if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_SPACE:
                polys.append(Polygon(mpoints, (255, 255, 255)))
                print("Polygon added")
                mpoints = []
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mpoints.append(Point(event.pos))
            print("point added")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            with open("map.csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'r', 'g', 'b'])
                for poly in polys:
                    csvwriter.writerow(poly.csvexport())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse3Down = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            mouse3Down = False
        if mouse3Down:
            for poly in polys:
                for point in poly.points:
                    if point.touching(pygame.mouse.get_pos()) == True:
                        print("hi")
                        point.center = (event.pos)
            pass

    for point in mpoints:
        point.draw(screen,(255,0,0))
    for poly in polys:
        poly.draw(screen)
    # Rendering
    pygame.display.flip()

pygame.quit()
