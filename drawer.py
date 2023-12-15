import pygame
from pygame import gfxdraw
import math
import csv
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
fps = 60
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
    def touched(self,event):
        if "mouse3Down" in heldbuttons:
            point.center = (event.pos)

class vslider:
    def __init__(self, state, location, length, width, range): #locatoin is top middle
        self.state = state
        self.location = location
        self.length = length
        self.width = width
        self.range = range
    def draw(self,screen):
        sliderX ,sliderY = self.location
        sliderX-= self.width/2
        pygame.draw.rect(screen,(100,100,100), (sliderX, sliderY, 20, self.length), self.width)
        pygame.draw.circle(screen, (200,200,200), self.handleLocation(), ((self.width+(self.width*self.state)/2)))
    def touching(self, collidee):
        collideeX, collideeY = collidee
        #handle
        centerX, centerY = self.handleLocation()
        if math.sqrt((collideeX - centerX) ** 2 + (collideeY - centerY) ** 2) <= ((self.width+(self.width*self.state)/2)):
            return True
        #slider
        sliderTX, sliderTY = self.location
        sliderTX -= self.width / 2
        sliderBX = sliderTX + self.width
        sliderBY = sliderTY - self.length
        print(f"{sliderTX,sliderTY}-{sliderBX,sliderBY}")
        if sliderTX <= collideeX <= sliderBX and sliderTY <= collideeY <= sliderBY:
            return True
        return False
    def touched(self,event):

        if "mouse3Down" in heldbuttons:
            print("hi")
            handleX, handleY = self.handleLocation()
            mouseX,mouseY = (event.pos)
            differnce = mouseY - handleY
            self.state = 1 - (mouseY - self.location[1]) / self.length
            self.state = max(0, min(1, self.state))

    def handleLocation(self):
        topX,topY = self.location
        return (topX,(topY+(self.length-(self.length*self.state))))
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
        # TODO make poly export
        x1,y1,x2,y2,x3,y3= (self.points[0].center[0],self.points[0].center[1],self.points[1].center[0],self.points[1].center[1],self.points[2].center[0],self.points[2].center[1],)  # ((x1,y1),(x2,y2),(x3,y3))
        r,g,b = self.color
        return(x1,y1,x2,y2,x3,y3,r,g,b)
    def csvimport(entry):
        #TODO make poly import
        x1, y1, x2, y2, x3, y3, r, g, b = map(int, entry)
        tripoints = [
            Point((x1, y1)),
            Point((x2, y2)),
            Point((x3, y3))
        ]
        polys.append(Polygon(tripoints, (r, g, b)))
#TODO make ui
ui=[]
ui.append(vslider(0,(100,100),200,20,255))
polys = []
mpoints = []
heldbuttons=[]
while running:
    screen.fill((0, 0, 0))
    # Input
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
            heldbuttons.append("mouse3Down")
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            heldbuttons.remove("mouse3Down")
        for poly in polys:
            for point in poly.points:
                if point.touching(pygame.mouse.get_pos()) == True:
                    point.touched(event)
        for element in ui:
            if element.touching(pygame.mouse.get_pos()) == True:
                element.touched(event)

    # Rendering
    for point in mpoints:
        point.draw(screen,(255,0,0))
    for poly in polys:
        poly.draw(screen)
    for element in ui:
        element.draw(screen)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
