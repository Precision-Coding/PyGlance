import numpy as np
import pygame as py

class Camera():
    def __init__(self):
        self.position_vector = np.array([0, 0, -500])
        self.direction_vector = np.array([0, 0, 1])
        self.FOV = np.pi/2
        self.leftboundingbox = np.array(np.matmul(self.direction_vector, np.matrix(([np.cos(self.FOV/2), 0, np.sin(self.FOV/2)],[0, 1, 0],[-np.sin(self.FOV/2), 0, np.cos(self.FOV/2)]))))[0]
        self.rightboundingbox = np.array(np.matmul(self.direction_vector, np.matrix(([np.cos(-self.FOV/2), 0, np.sin(-self.FOV/2)],[0, 1, 0],[-np.sin(-self.FOV/2), 0, np.cos(-self.FOV/2)]))))[0]
        self.costhetamax = np.dot(self.leftboundingbox, self.rightboundingbox)
