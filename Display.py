import numpy as np
import pygame as pg

class Display():
    def __init__(self):
        self.run = True
        self.screen_height = 800
        self.screen_width = 1200
        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        self.clock = pg.time.Clock()
        self.fps = 120
