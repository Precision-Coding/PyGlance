import numpy as np
import pygame as pg
from Display import Display

class Render():

    def polygonPerspectiveProjection(self, polygon, camera, display):
        projection_coords = []

        for coordinates in polygon.vertices_coordinates:
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            coordinate_position_vector = coordinates
            coordinate_direction_vector = coordinates-camera.position_vector
            #project coordinate onto the clipping plane
            t = -(np.dot(camera.direction_vector, coordinate_position_vector)-camera.k)/np.dot(camera.direction_vector, coordinate_direction_vector)
            clipping_plane_coordinate = coordinate_position_vector + t*coordinate_direction_vector
            polygon.is_drawn = True
            #Set coordinates based on distance from bottom and left
            horizontal_plane_coordinate_distance = np.linalg.norm(np.cross(camera.direction_vector_up, clipping_plane_coordinate-camera.left_bounding_coordinate))
            horizontal_plane_coordinate_distance_R = np.linalg.norm(np.cross(camera.direction_vector_up, clipping_plane_coordinate-camera.right_bounding_coordinate))
            vertical_plane_coordinate_distance = np.linalg.norm(np.cross(camera.direction_vector_right, clipping_plane_coordinate-camera.bottom_bounding_coordinate))
            vertical_plane_coordinate_distance_T = np.linalg.norm(np.cross(camera.direction_vector_right, clipping_plane_coordinate-camera.top_bounding_coordinate))
            clipping_plane_height = np.linalg.norm(np.cross(camera.direction_vector_right, camera.top_bounding_coordinate-camera.bottom_bounding_coordinate))
            clipping_plane_width = np.linalg.norm(np.cross(camera.direction_vector_up, camera.right_bounding_coordinate-camera.left_bounding_coordinate))
            if horizontal_plane_coordinate_distance > clipping_plane_width or horizontal_plane_coordinate_distance_R > clipping_plane_width:
                polygon.is_drawn = False
            elif vertical_plane_coordinate_distance > clipping_plane_height or vertical_plane_coordinate_distance_T > clipping_plane_height:
                polygon.is_drawn = False
            x_coordinate = horizontal_plane_coordinate_distance / clipping_plane_width * display.screen_width
            y_coordinate = vertical_plane_coordinate_distance / clipping_plane_height * display.screen_height
           #Translates angle into screen coordinates
            projection_coords.append([x_coordinate, y_coordinate])

        return (projection_coords[0], projection_coords[1], projection_coords[2])

    def pygameDrawModel(self, display, camera, model):
        #transforms the polygons
        for polygon in model.polygon_array:
            polygon.rotate(model.pitch, model.yaw, model.roll)
            polygon.cos_theta = np.dot(camera.direction_vector, polygon.normal)

        #sorts the polygons
        polygons = sorted(model.polygon_array, key=lambda polygon: -np.linalg.norm(polygon.middle_coordinate-camera.position_vector))

        #projects and draws the polygons
        for polygon in polygons:
            if polygon.cos_theta > 0:
                polygon.colour = (polygon.cos_theta*225, polygon.cos_theta*225, polygon.cos_theta*225)
                pg.draw.polygon(display.screen, polygon.colour, self.polygonPerspectiveProjection(polygon, camera, display))
