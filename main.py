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
    display.psi = 0.0
    display.phi = 0.05
    display.theta = 0.0
    #transforms the polygons
    for polygon in polygons:
        polygon.rotate(display.phi, display.theta, display.psi)
        costheta = (np.dot(display.cameravector, polygon.normal)/np.linalg.norm(polygon.normal)/np.linalg.norm(display.cameravector))
        if costheta > 0:
            polygon.isdrawn = False
        else:
            polygon.isdrawn = True
    #sorts the polygons
    polygons = sorted(polygons, key=lambda polygon: -np.linalg.norm(polygon.coordmid-display.camera))
    #projects and draws the polygons
    for polygon in polygons:
        if polygon.isdrawn:
            polygon.perspective_projection(polygon, display.cameravector, display.camera)
            dist = np.linalg.norm(polygon.coordmid-display.camera)
            if dist >= 0 and dist < 255:
                polygon.colour = (dist, 0, 0)
            elif dist >= 255 and dist < 510:
                polygon.colour = (255, dist-255, 0)
            elif dist >= 510 and dist < 765:
                polygon.colour = (255-(dist-510), 255, 0)
            elif dist >= 765 and dist < 1020:
                polygon.colour = (0, 255, dist-765)
            elif dist >= 1020 and dist < 1275:
                polygon.colour = (0, 255-(dist-1020), 255)
            elif dist >= 1275 and dist < 1530:
                polygon.colour = (dist-1020, dist-1275, 255)
            else:
                polygon.colour = (255, 255, 255)
            pg.draw.polygon(display.screen, polygon.colour, (polygon.projectedcoord1, polygon.projectedcoord2, polygon.projectedcoord3))
            pg.draw.polygon(display.screen, "black", (polygon.projectedcoord1, polygon.projectedcoord2, polygon.projectedcoord3), 1)
    pg.display.flip()