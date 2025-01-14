import numpy as np
import pygame as pg
from Display import Display

class Polygon:
    def __init__(self, coordinate1, coordinate2, coordinate3, normal, colour, display):
        self.coord1 = coordinate1
        self.coord2 = coordinate2
        self.coord3 = coordinate3
        self.normal = -normal
        middlecoordinate = (coordinate1+coordinate2+coordinate3)/3
        self.coordmid = middlecoordinate
        self.colour = colour
        #placeholders for when they are assigned later lol
        self.projectedcoord1 = np.array([0, 0])
        self.projectedcoord2 = np.array([0, 0])
        self.projectedcoord3 = np.array([0, 0])
        self.display = display
        self.isdrawn = True
        self.costheta = 1

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

