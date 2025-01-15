import numpy as np
import pygame as pg
from Display import Display

class Render():

    def polygonPerspectiveProjection(self, polygon, camera, display):
        projection_coords = []

        for coordinates in polygon.vertices_coordinates:
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            vertical_coordinate = np.array([0, coordinates[1], coordinates[2]])
            vertical_vector = vertical_coordinate-camera.position_vector
            #Horizontalcoordinate = np.array([coordinates[0], 0, coordinates[2]]) have a good ponder later
            general_vector = coordinates-camera.position_vector
            cos_theta_left = np.dot(camera.left_bounding_box, general_vector)/(np.linalg.norm(camera.left_bounding_box)*np.linalg.norm(general_vector))
            cos_theta_right = np.dot(camera.right_bounding_box, general_vector)/(np.linalg.norm(camera.right_bounding_box)*np.linalg.norm(general_vector))
            vertical_angle = ((np.dot(camera.direction_vector, vertical_vector))/(np.linalg.norm(camera.direction_vector)*np.linalg.norm(vertical_vector)))
            if cos_theta_right < camera.cos_theta_max or cos_theta_left < camera.cos_theta_max:
                polygon.is_drawn = False
                x_coordinate = (0, 0, 0)
            else:
                polygon.is_drawn = True
                x_coordinate = np.arccos(cos_theta_left)/camera.fov*display.screen_width

       #Translates angle into screen coordinates
            y_coordinate = np.arccos(vertical_angle)/(camera.fov/2) * (display.screen_height//2) + (display.screen_height//2)
            projection_coords.append([x_coordinate, y_coordinate])

        return (projection_coords[0], projection_coords[1], projection_coords[2])

    def pygameDrawModel(self, display, camera, model):
        #transforms the polygons
        for polygon in model.polygon_array:
            polygon.rotate(model.pitch, model.yaw, model.roll)
            polygon.cos_theta = (np.dot(camera.direction_vector, polygon.normal)/np.linalg.norm(polygon.normal)/np.linalg.norm(camera.direction_vector))

        #sorts the polygons
        polygons = sorted(model.polygon_array, key=lambda polygon: -np.linalg.norm(polygon.middle_coordinate-camera.position_vector))

        #projects and draws the polygons
        for polygon in polygons:
            if polygon.cos_theta > 0:
                polygon.colour = (polygon.cos_theta*225, polygon.cos_theta*225, polygon.cos_theta*225)
                pg.draw.polygon(display.screen, polygon.colour, self.polygonPerspectiveProjection(polygon, camera, display))
