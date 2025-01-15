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
frameCount = 0

start = time.time()
while display.run:
    frameCount += 1
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            display.run = False
    display.screen.fill("white")
    render.pygameDrawModel(display, camera, model)

    print(round(frameCount/(time.time() - start), 1))
    pg.display.flip()
    display.clock.tick(display.fps)