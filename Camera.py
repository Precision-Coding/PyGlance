import numpy as np
import pygame as py

class Camera():
    def __init__(self):
        self.position_vector = np.array([0, 0, 200])
        self.roll = 0
        self.pitch = 0
        self.yaw = 0
