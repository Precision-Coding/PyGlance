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
fpslist = []
while display.run:
    #Event loop
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            display.run = False
    start = time.time()
    display.clock.tick(display.fps)
    display.screen.fill("white")
    render.pygameDrawModel(display, camera, model)
    end = time.time()
    framespersecond = 1/(end-start)
    fpslist.append(framespersecond)
    sum = 0
    for i in fpslist:
        sum += i
    print(sum/len(fpslist))
    pg.display.flip()