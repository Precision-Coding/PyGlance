import pygame as pg
import numpy as np
pg.init()
run = True
SCREENWIDTH = 800
SCREENHEIGHT = 800
screen = pg.display.set_mode([SCREENWIDTH, SCREENHEIGHT]) #Creates display for user
clock = pg.time.Clock()
FPS = 60
camera = np.array([0, 0, -1000])
cameravector = np.array([0, 0, 1])
phi = np.pi/8
theta = np.pi/8
FOV = np.pi/3

class Polygon:
    def __init__(self, coordinate1, coordinate2, coordinate3, colour):
        self.coord1 = coordinate1
        self.coord2 = coordinate2
        self.coord3 = coordinate3
        middlecoordinate = (coordinate1+coordinate2+coordinate3)/3
        self.coordmid = middlecoordinate
        self.colour = colour
        #placeholders for when they are assigned later lol
        self.projectedcoord1 = np.array([0, 0])
        self.projectedcoord2 = np.array([0, 0])
        self.projectedcoord3 = np.array([0, 0])

    def rotate(self, phi, theta):
        rotationXMatrix = [[1, 0, 0], [0, np.cos(phi), -np.sin(phi)], [0, np.sin(phi), np.cos(phi)]]
        rotationYMatrix = [[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]]
        self.coord1 = np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.coord1))
        self.coord2 = np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.coord2))
        self.coord3 = np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.coord3))
        return self.coord1, self.coord2, self.coord3

    def draw(self):
        pg.draw.polygon(screen, "grey", (self.projectedcoord1, self.projectedcoord2, self.projectedcoord3))
        pg.draw.polygon(screen, "black", (self.projectedcoord1, self.projectedcoord2, self.projectedcoord3), 5)

    def perspective_projection(self, polygon, cameravector):
        polygoncoords = [self.coord1, self.coord2, self.coord3]
        projectioncoords = []
        for coordinates in polygoncoords:
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            verticalcoordinate = np.array([0, coordinates[1], coordinates[2]])
            verticalvector = verticalcoordinate-camera
            horizontalcoordinate = np.array([coordinates[0], 0, coordinates[2]])
            horizontalvector = horizontalcoordinate-camera

            #Manually assigns +/- signs to calulated angle between the 2 vectors
            if coordinates[1] >= 0:
                verticalangle = np.arccos((np.dot(cameravector, verticalvector))/(np.linalg.norm(cameravector)*np.linalg.norm(verticalvector)))
            else:
                verticalangle = -np.arccos((np.dot(cameravector, verticalvector))/(np.linalg.norm(cameravector)*np.linalg.norm(verticalvector)))

            if coordinates[0] >= 0:
                horizontalangle = np.arccos((np.dot(cameravector, horizontalvector))/(np.linalg.norm(cameravector)*np.linalg.norm(horizontalvector)))
            else:
                horizontalangle = -np.arccos((np.dot(cameravector, horizontalvector))/(np.linalg.norm(cameravector)*np.linalg.norm(horizontalvector)))

            #Translates angle into screen coordinates
            xcoordinate = horizontalangle/(FOV/2) * (SCREENWIDTH//2) + (SCREENWIDTH//2)
            ycoordinate = verticalangle/(FOV/2) * (SCREENHEIGHT//2) + (SCREENHEIGHT//2)
            projectioncoords.append([xcoordinate, ycoordinate])
        self.projectedcoord1 = projectioncoords[0]
        self.projectedcoord2 = projectioncoords[1]
        self.projectedcoord3 = projectioncoords[2]
polygon1 = Polygon(np.array([0, 100, 0]), np.array([86, -50, 0]), np.array([-86, -50, 0]), "red")
polygon2 = Polygon(np.array([0, 0, 100]), np.array([86, -50, 0]), np.array([-86, -50, 0]), "red") 
polygon3 = Polygon(np.array([0, 100, 0]), np.array([0, 0, 100]), np.array([-86, -50, 0]), "red")
polygon4 = Polygon(np.array([0, 100, 0]), np.array([86, -50, 0]), np.array([0, 0, 100]), "red")
polygons = [polygon1, polygon2, polygon3, polygon4]
while run:
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    clock.tick(FPS)
    screen.fill("white")
    phi = 0.01
    theta = 0.01

    for polygon in polygons:
        polygon.rotate(phi, theta)
        polygon.perspective_projection(polygon, cameravector)
        polygon.draw()

    pg.display.flip()