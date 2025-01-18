import numpy as np
import pygame as pg
from Display import Display
class Polygon:
    def __init__(self, vertices_coordinates, normal, colour):
        self.vertices_coordinates = vertices_coordinates
        self.normal = normal
        self.middle_coordinate = (vertices_coordinates[0] + vertices_coordinates[1] + vertices_coordinates[2])/3
        self.colour = colour
        #placeholders for when they are assigned later lol
        self.is_drawn = True
        self.cos_theta = 1

    def rotate(self, pitch, yaw, roll):

        rotation_x_matrix = [[1, 0, 0],
                           [0, np.cos(pitch), -np.sin(pitch)],
                           [0, np.sin(pitch), np.cos(pitch)]]

        rotation_y_matrix = [[np.cos(yaw), 0, np.sin(yaw)],
                           [0, 1, 0],
                           [-np.sin(yaw), 0, np.cos(yaw)]]

        rotation_z_matrix = [[np.cos(roll), -np.sin(roll), 0],
                           [np.sin(roll), np.cos(roll), 0],
                           [0, 0, 1]]

        self.vertices_coordinates[0] = np.matmul(rotation_z_matrix, np.matmul(rotation_x_matrix, np.matmul(rotation_y_matrix, self.vertices_coordinates[0])))
        self.vertices_coordinates[1] = np.matmul(rotation_z_matrix, np.matmul(rotation_x_matrix, np.matmul(rotation_y_matrix, self.vertices_coordinates[1])))
        self.vertices_coordinates[2] = np.matmul(rotation_z_matrix, np.matmul(rotation_x_matrix, np.matmul(rotation_y_matrix, self.vertices_coordinates[2])))
        self.normal = np.matmul(rotation_z_matrix, np.matmul(rotation_x_matrix, np.matmul(rotation_y_matrix, self.normal)))
        self.middle_coordinate = (self.vertices_coordinates[0] + self.vertices_coordinates[1] + self.vertices_coordinates[2])/3
