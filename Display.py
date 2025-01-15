import numpy as np
import pygame as pg

class Display():
    def __init__(self):
        self.run = True
        self.screen_height = 800
        self.screen_width = 800
        self.screen = pg.display.set_mode([self.screen_height, self.screen_width])
        self.clock = pg.time.Clock()
        self.fps = 60
