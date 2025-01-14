import numpy as np
import pygame as py

class Camera():
    def __init__(self):
        self.position_vector = np.array([0, 0, -500])
        self.direction_vector = np.array([0, 0, 1])
        self.fov = np.pi/2
        self.left_bounding_box = np.array(np.matmul(self.direction_vector, np.matrix(([np.cos(self.fov/2), 0, np.sin(self.fov/2)],[0, 1, 0],[-np.sin(self.fov/2), 0, np.cos(self.fov/2)]))))[0]
        self.right_bounding_box = np.array(np.matmul(self.direction_vector, np.matrix(([np.cos(-self.fov/2), 0, np.sin(-self.fov/2)],[0, 1, 0],[-np.sin(-self.fov/2), 0, np.cos(-self.fov/2)]))))[0]
        self.cos_theta_max = np.dot(self.left_bounding_box, self.right_bounding_box)
