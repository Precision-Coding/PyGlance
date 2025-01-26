# main.py
from DependencyInstaller import *

if __name__ == "__main__":
    # Ensure dependencies are checked first
    print("Checking and installing Python dependencies...")
    check_and_install_dependencies()

    print("\nAll setup steps completed successfully!")


import pygame as pg
import numpy as np
from Display import Display
from Camera import Camera
from Polygon import Polygon
from Model import Model
import time
pg.init()
camera = Camera()
display = Display()
model = Model("STLFiles/CatLowPoly.stl", (0, 0, 50))
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

    camera.rotate()
    display.screen.fill("white")
    model.render(camera, display)
    for polygon in model.polygon_array:
        if polygon.is_drawn:
            pg.draw.polygon(display.screen, polygon.colour, polygon.vertices_projection_coords)

    if frameCount % 60 == 0:
        print(int(round(frameCount/(time.time() - start), 0)))
    pg.display.flip()
    display.clock.tick(display.fps)