import pygame as pg
import numpy as np
from Display import Display
from Camera import Camera
from Polygon import Polygon
from Model import Model
from Render import Render
import time
pg.init()
camera = Camera()
display = Display()
render = Render()
model = Model()

polygons = model.polygon_array

while display.run:
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            display.run = False

    display.clock.tick(display.fps)
    display.screen.fill("white")
    #transforms the polygons
    for polygon in polygons:
        polygon.rotate(display.pitch, display.yaw, display.roll)
        polygon.cos_theta = (np.dot(camera.direction_vector, polygon.normal)/np.linalg.norm(polygon.normal)/np.linalg.norm(camera.direction_vector))

    #sorts the polygons
    polygons = sorted(polygons, key=lambda polygon: -np.linalg.norm(polygon.middle_coordinate-camera.position_vector))
    #projects and draws the polygons
    for polygon in polygons:
        if polygon.cos_theta > 0:
            polygon.colour = (polygon.cos_theta*225, polygon.cos_theta*225, polygon.cos_theta*225)
            pg.draw.polygon(display.screen, polygon.colour, render.polygonPerspectiveProjection(polygon, camera, display))

    pg.display.flip()