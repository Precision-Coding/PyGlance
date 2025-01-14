import numpy as np
import pygame as pg
import Display as display

class Polygon:
    def __init__(self, coordinate1, coordinate2, coordinate3, normal, colour, display):
        self.coord1 = coordinate1
        self.coord2 = coordinate2
        self.coord3 = coordinate3
        self.normal = normal
        middlecoordinate = (coordinate1+coordinate2+coordinate3)/3
        self.coordmid = middlecoordinate
        self.colour = colour
        #placeholders for when they are assigned later lol
        self.projectedcoord1 = np.array([0, 0])
        self.projectedcoord2 = np.array([0, 0])
        self.projectedcoord3 = np.array([0, 0])
        self.display = display
        self.isdrawn = True

    def rotate(self, phi, theta, psi):

        rotationXMatrix = [[1, 0, 0],
                           [0, np.cos(phi), -np.sin(phi)],
                           [0, np.sin(phi), np.cos(phi)]]

        rotationYMatrix = [[np.cos(theta), 0, np.sin(theta)],
                           [0, 1, 0],
                           [-np.sin(theta), 0, np.cos(theta)]]

        rotationZMatrix = [[np.cos(psi), -np.sin(psi), 0],
                           [np.sin(psi), np.cos(psi), 0],
                           [0, 0, 1]]

        self.coord1 = np.matmul(rotationZMatrix, np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.coord1)))
        self.coord2 = np.matmul(rotationZMatrix, np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.coord2)))
        self.coord3 = np.matmul(rotationZMatrix, np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.coord3)))
        self.normal = np.matmul(rotationZMatrix, np.matmul(rotationXMatrix, np.matmul(rotationYMatrix, self.normal)))
        middlecoordinate = (self.coord1+self.coord2+self.coord3)/3
        self.coordmid = middlecoordinate
        return self.coord1, self.coord2, self.coord3

    def draw(self, screen):
        pg.draw.polygon(screen, self.colour, (self.projectedcoord1, self.projectedcoord2, self.projectedcoord3))
        pg.draw.polygon(screen, "black", (self.projectedcoord1, self.projectedcoord2, self.projectedcoord3), 5)

    def perspective_projection(self, polygon, cameravector, camera):
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
            xcoordinate = horizontalangle/(self.display.FOV/2) * (self.display.screen_height//2) + (self.display.screen_height//2)
            ycoordinate = verticalangle/(self.display.FOV/2) * (self.display.screen_height//2) + (self.display.screen_height//2)
            projectioncoords.append([xcoordinate, ycoordinate])

        self.projectedcoord1 = projectioncoords[0]
        self.projectedcoord2 = projectioncoords[1]
        self.projectedcoord3 = projectioncoords[2]