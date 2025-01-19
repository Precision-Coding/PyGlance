import numpy as np
from numpy import cos as c
from numpy import sin as s
import pygame as pg
from Display import Display
class Polygon:
    def __init__(self, vertices_coordinates, normal):
        self.vertices_coordinates = vertices_coordinates
        self.normal = normal
        self.middle_coordinate = (vertices_coordinates[0] + vertices_coordinates[1] + vertices_coordinates[2])/3
        self.colour = ()
        #placeholders for when they are assigned later lol
        self.is_drawn = True
        self.cos_theta = 1

    def rotate(self, x, y, z):
        #x = pitch, y = yaw, z = roll
        rotation_matrix = np.array([
            np.array([c(y)*c(z), -c(y)*s(z), s(y)]),
            np.array([c(x)*s(z)+s(x)*s(y)*c(z), c(x)*c(z)-s(x)*s(y)*s(z), -s(x)*c(y)]),
            np.array([s(x)*s(z)-c(x)*s(y)*c(z), s(x)*c(z)+c(x)*s(y)*s(z), c(x)*c(y)])
        ])

        for i in range(0,3):
            self.vertices_coordinates[i] = np.matmul(rotation_matrix, self.vertices_coordinates[i])

