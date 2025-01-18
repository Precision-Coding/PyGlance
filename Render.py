import numpy as np
import pygame as pg
from Display import Display

class Render():

    def polygonPerspectiveProjection(self, polygon, camera, display):
        projection_coords = []

        for coordinates in polygon.vertices_coordinates:
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            translated_coordinates = coordinates - camera.position_vector
            transformed_coordinates = np.matmul(translated_coordinates, camera.rotation_matrix)
            x_coordinate = transformed_coordinates[0]/-transformed_coordinates[2] * 100 + display.screen_width/2
            y_coordinate = transformed_coordinates[1]/-transformed_coordinates[2] * 100 + display.screen_height/2
            projection_coords.append([x_coordinate, y_coordinate])

        return (projection_coords[0], projection_coords[1], projection_coords[2])

    def polygonShadingAndCulling(self, polygon, camera, model):
        transformed_midpoint = polygon.middle_coordinate-camera.position_vector
        cos_theta = np.dot(transformed_midpoint, polygon.normal)/np.linalg.norm(transformed_midpoint) #cos theta = (a.b)/|a||b|

        if cos_theta < 0:
            polygon.colour = (model.colour[0] * -cos_theta, model.colour[1] * -cos_theta, model.colour[2] * -cos_theta)
            polygon.is_drawn = True
        else:
            polygon.is_drawn = False

    def pygameDrawModel(self, display, camera, model):
        #transforms the polygons shades and culls backfacing
        for polygon in model.polygon_array:
            polygon.rotate(model.pitch, model.yaw, model.roll)
            self.polygonShadingAndCulling(polygon, camera, model)

        #sorts the polygons
        polygons = sorted(model.polygon_array, key=lambda polygon: np.linalg.norm(polygon.middle_coordinate-camera.position_vector), reverse=True)

        #projects and draws the polygons
        for polygon in polygons:
            if polygon.is_drawn:
                pg.draw.polygon(display.screen, polygon.colour, self.polygonPerspectiveProjection(polygon, camera, display))
