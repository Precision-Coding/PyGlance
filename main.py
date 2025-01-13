import pygame as pg
import numpy as np
from Display import Display
from Polygon import Polygon
pg.init()

display = Display()

polygon1 = Polygon(np.array([0, 100, 0]), np.array([86, -50, 0]), np.array([-86, -50, 0]), "red", display)
polygon2 = Polygon(np.array([0, 0, 100]), np.array([86, -50, 0]), np.array([-86, -50, 0]), "green", display)
polygon3 = Polygon(np.array([0, 100, 0]), np.array([0, 0, 100]), np.array([-86, -50, 0]), "blue", display)
polygon4 = Polygon(np.array([0, 100, 0]), np.array([86, -50, 0]), np.array([0, 0, 100]), "yellow", display)
polygons = [polygon1, polygon2, polygon3, polygon4]

while display.run:
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            display.run = False

    display.clock.tick(display.FPS)
    display.screen.fill("white")
    display.psi = 0.00
    display.phi = 0.01
    display.theta = 0.0

    #transforms the polygons
    for polygon in polygons:
        polygon.rotate(display.phi, display.theta, display.psi)
    #sorts the polygons
    polygons = sorted(polygons, key=lambda polygon: -np.linalg.norm(polygon.coordmid-display.camera))
    #projects and draws the polygons
    for polygon in polygons:
        polygon.perspective_projection(polygon, display.cameravector, display.camera)
        polygon.draw(display.screen)

    pg.display.flip()