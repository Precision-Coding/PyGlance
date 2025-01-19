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
    key_press = pg.key.get_pressed()
    camera_speed_multiplier = 2
    camera_turn_multiplier = 0.5
    if key_press[pg.K_w]:
        camera.position_vector += camera.forward * camera_speed_multiplier
    if key_press[pg.K_a]:
        camera.position_vector -= camera.right * camera_speed_multiplier
    if key_press[pg.K_s]:
        camera.position_vector -= camera.forward * camera_speed_multiplier
    if key_press[pg.K_d]:
        camera.position_vector += camera.right * camera_speed_multiplier
    if key_press[pg.K_LSHIFT]:
        camera.position_vector += np.array((0, -1, 0)) * camera_speed_multiplier
    if key_press[pg.K_LCTRL]:
        camera.position_vector += np.array((0, 1, 0)) * camera_speed_multiplier
    if key_press[pg.K_LEFT]:
        camera.yaw -= 0.1 * camera_turn_multiplier
    if key_press[pg.K_RIGHT]:
        camera.yaw += 0.1 * camera_turn_multiplier
    if key_press[pg.K_UP]:
        camera.pitch = min(max(camera.pitch + 0.1 * camera_turn_multiplier, -np.pi/2), np.pi/2)
    if key_press[pg.K_DOWN]:
        camera.pitch = min(max(camera.pitch - 0.1 * camera_turn_multiplier, -np.pi/2), np.pi/2)
    display.screen.fill("white")
    render.pygameDrawModel(display, camera, model)
    camera.pitch += 0.0
    camera.rotate()

    print(round(frameCount/(time.time() - start), 1))
    pg.display.flip()
    display.clock.tick(display.fps)