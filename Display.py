import numpy as np
import pygame as pg

class Display():
    def __init__(self):
        self.run = True
        self.screen_height = 800
        self.screen_width = 800
        self.screen = pg.display.set_mode([self.screen_height, self.screen_width])
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.camera = np.array([0, 0, -1000])
        self.cameravector = np.array([0, 0, 1])
        self.phi = np.pi/8
        self.theta = np.pi/8
        self.psi = np.pi/8
        self.FOV = np.pi/8
