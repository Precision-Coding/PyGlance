import numpy as np
import pygame as pg
from Display import Display

class Render():

    def polygonPerspectiveProjection(self, polygon, camera, display):
        polygoncoords = [polygon.coord1, polygon.coord2, polygon.coord3]
        projectioncoords = []

        for coordinates in polygoncoords:
            #finds horizontal and vertical components of vector 'camera' -> 'coordinate'
            verticalcoordinate = np.array([0, coordinates[1], coordinates[2]])
            verticalvector = verticalcoordinate-camera.position_vector
            horizontalcoordinate = np.array([coordinates[0], 0, coordinates[2]])
            horizontalvector = horizontalcoordinate-camera.position_vector
            generalvector = coordinates-camera.position_vector
            costhetaleft = np.dot(camera.leftboundingbox, generalvector)/(np.linalg.norm(camera.leftboundingbox)*np.linalg.norm(generalvector))
            costhetaright = np.dot(camera.rightboundingbox, generalvector)/(np.linalg.norm(camera.rightboundingbox)*np.linalg.norm(generalvector))
            verticalangle = ((np.dot(camera.direction_vector, verticalvector))/(np.linalg.norm(camera.direction_vector)*np.linalg.norm(verticalvector)))
            if costhetaright < camera.costhetamax or costhetaleft < camera.costhetamax:
                polygon.isdrawn = False
                xcoordinate = (0, 0, 0)
            else:
                polygon.isdrawn = True
                xcoordinate = np.arccos(costhetaleft)/camera.FOV*display.screen_width

       #Translates angle into screen coordinates
            ycoordinate = np.arccos(verticalangle)/(camera.FOV/2) * (display.screen_height//2) + (display.screen_height//2)
            projectioncoords.append([xcoordinate, ycoordinate])

        return (projectioncoords[0], projectioncoords[1], projectioncoords[2])