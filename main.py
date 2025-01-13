import pygame as pg
import numpy as np
from Display import Display
from Polygon import Polygon
pg.init()

display = Display()

polygon1 = Polygon(coordinate1=np.array((100, 100, -100)), coordinate2=np.array((-100, 100, -100)), coordinate3=np.array((100, -100, -100)), normal=((1, 0, 0)), colour="red", display=display)
polygon2 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon3 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon4 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon5 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon6 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon7 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon8 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon9 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon10 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon11 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)
polygon12 = Polygon(coordinate1=np.array((0, 0, 0)), coordinate2=np.array((0, 0, 0)), coordinate3=np.array((0, 0, 0)), normal=((1, 0, 0)), colour="red", display=display)


polygons = [polygon1]

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