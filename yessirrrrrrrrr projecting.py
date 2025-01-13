import pygame as pg
import numpy as np
from Display import Display
from Polygon import Polygon
pg.init()

display = Display()

polygon1 = Polygon(np.array([0, 100, 0]), np.array([86, -50, 0]), np.array([-86, -50, 0]), "red", display)
polygon2 = Polygon(np.array([0, 0, 100]), np.array([86, -50, 0]), np.array([-86, -50, 0]), "red", display)
polygon3 = Polygon(np.array([0, 100, 0]), np.array([0, 0, 100]), np.array([-86, -50, 0]), "red", display)
polygon4 = Polygon(np.array([0, 100, 0]), np.array([86, -50, 0]), np.array([0, 0, 100]), "red", display)
polygons = [polygon1, polygon2, polygon3, polygon4]

while display.run:
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            display.run = False

    display.clock.tick(display.FPS)
    display.screen.fill("white")
    phi = 0.01
    theta = 0.01

    for polygon in polygons:
        polygon.rotate(phi, theta)
        polygon.perspective_projection(polygon, display.cameravector, display.camera)
        polygon.draw(display.screen)

    pg.display.flip()