import numpy as np
from numpy import cos
from numpy import sin
import pygame as pg
from Display import Display
class Polygon:
    def __init__(self, vertices_coordinates, normal):
        self.vertices_coordinates = vertices_coordinates
        self.normal = normal
        self.middle_coordinate = (vertices_coordinates[0] + vertices_coordinates[1] + vertices_coordinates[2])/3
        self.colour = np.array(())
        self.is_drawn = True
        self.cos_theta = 1
        self.vertices_projection_coords = np.array((np.array((0, 0)), np.array((0, 0)), np.array((0, 0))))

    def rotate(self, pitch, yaw, roll):
        rotation_matrix = np.array([
            np.array([cos(yaw)*cos(roll), -cos(yaw)*sin(roll), sin(yaw)]),
            np.array([cos(pitch)*sin(roll)+sin(pitch)*sin(yaw)*cos(roll), cos(pitch)*cos(roll)-sin(pitch)*sin(yaw)*sin(roll), -sin(pitch)*cos(yaw)]),
            np.array([sin(pitch)*sin(roll)-cos(pitch)*sin(yaw)*cos(roll), sin(pitch)*cos(roll)+cos(pitch)*sin(yaw)*sin(roll), cos(pitch)*cos(yaw)])
        ])

        for i in range(0,3):
            self.vertices_coordinates[i] = np.matmul(rotation_matrix, self.vertices_coordinates[i])

    def shade(self, camera, colour):
        transformed_midpoint = self.middle_coordinate-camera.position_vector
        cos_theta = np.dot(transformed_midpoint, self.normal)/np.linalg.norm(transformed_midpoint) #cos theta = (a.b)/|a||b|

        if cos_theta < 0:
            self.colour = (colour[0] * -cos_theta, colour[1] * -cos_theta, colour[2] * -cos_theta)
            self.is_drawn = True
        else:
            self.is_drawn = False

    def project(self, camera, display):
        for arrayIndex, coordinates in enumerate(self.vertices_coordinates):
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            translated_coordinates = coordinates - camera.position_vector
            transformed_coordinates = np.matmul(translated_coordinates, camera.rotation_matrix)
            x_coordinate = transformed_coordinates[0]/-transformed_coordinates[2] * 300 + display.screen_width/2
            y_coordinate = transformed_coordinates[1]/-transformed_coordinates[2] * 300 + display.screen_height/2
            self.vertices_projection_coords[arrayIndex] = np.array((x_coordinate, y_coordinate))

    #Culls drawing polygons if offscreen
    def cull(self, display):
        off_screen_vertecies_count = 0
        for coordinates in self.vertices_projection_coords:
            if coordinates[0] > display.screen_width or coordinates[1] > display.screen_height or coordinates[0] < 0 or coordinates[1] < 0:
                off_screen_vertecies_count += 1

        if off_screen_vertecies_count == 3:
            self.is_drawn = False