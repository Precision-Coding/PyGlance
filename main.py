import pygame as pg
import numpy as np
from Display import Display
from Polygon import Polygon
from Model import Model
import time
pg.init()

display = Display()

model = Model(display)

polygons = model.PolygonArray

while display.run:
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            display.run = False

    display.clock.tick(display.FPS)
    display.screen.fill("white")
    display.psi = 0.00
    display.phi = 0.00
    display.theta = 0.05
    #transforms the polygons
    for polygon in polygons:
        polygon.rotate(display.phi, display.theta, display.psi)
        polygon.costheta = (np.dot(display.cameravector, polygon.normal)/np.linalg.norm(polygon.normal)/np.linalg.norm(display.cameravector))

    #sorts the polygons
    polygons = sorted(polygons, key=lambda polygon: -np.linalg.norm(polygon.coordmid-display.camera))
    #projects and draws the polygons
    for polygon in polygons:
        if polygon.costheta > 0:
            polygon.perspective_projection(polygon, display.cameravector, display.camera)
            polygon.colour = (polygon.costheta*225, polygon.costheta*225, polygon.costheta*225)
            pg.draw.polygon(display.screen, polygon.colour, (polygon.projectedcoord1, polygon.projectedcoord2, polygon.projectedcoord3))

    pg.display.flip()