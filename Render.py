import numpy as np
import pygame as pg
from Display import Display

class Render():

    def polygonPerspectiveProjection(self, polygon, camera, display):
        projection_coords = []

        for coordinates in polygon.vertices_coordinates:
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            transformed_coordinates = coordinates - camera.position_vector
            x_coordinate = transformed_coordinates[0]/-transformed_coordinates[2] * 700 + display.screen_width/2
            y_coordinate = transformed_coordinates[1]/-transformed_coordinates[2] * 700 + display.screen_height/2
            projection_coords.append([x_coordinate, y_coordinate])

        transformed_midpoint = polygon.middle_coordinate-camera.position_vector
        cos_theta = np.dot(transformed_midpoint, polygon.normal)/np.linalg.norm(transformed_midpoint) #cos theta = (a.b)/|a||b|
        if cos_theta < 0:
            polygon.colour = (abs(200*cos_theta), abs(200*cos_theta), abs(200*cos_theta))
            polygon.is_drawn = True
        else:
            polygon.colour = "red"
            polygon.is_drawn = False

        return (projection_coords[0], projection_coords[1], projection_coords[2])

    def pygameDrawModel(self, display, camera, model):
        #transforms the polygons
        for polygon in model.polygon_array:
            polygon.rotate(model.pitch, model.yaw, model.roll)

        #sorts the polygons
        polygons = sorted(model.polygon_array, key=lambda polygon: -np.linalg.norm(polygon.middle_coordinate-camera.position_vector))

        #projects and draws the polygons
        for polygon in polygons:
            polygon_position = self.polygonPerspectiveProjection(polygon, camera, display)
            if polygon.is_drawn:
                pg.draw.polygon(display.screen, polygon.colour, polygon_position)
