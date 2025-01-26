import numpy as np
import pygame as py

class Camera():
    def __init__(self):
        self.position_vector = np.array([0., 0., -300.])
        self.pitch = 0
        self.yaw = np.pi
        self.rotation_matrix =np.array([ #Placeholder for when its set later
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([0, 0, 1])
        ])
        self.rotation_y_matrix =np.array([ #Placeholder for when its set later
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([0, 0, 1])
        ])
        self.up = np.array((0., 1., 0.))
        self.right = np.array((1., 0., 0.))
        self.forward = np.array((0., 0., -1.))

    def rotate(self):
        self.rotation_matrix =np.array([
            np.array([np.cos(-self.yaw), np.sin(-self.yaw) * np.sin(-self.pitch), np.sin(-self.yaw) * np.cos(-self.pitch)]),
            np.array([0, np.cos(-self.pitch), -np.sin(-self.pitch)]),
            np.array([-np.sin(-self.yaw), np.cos(-self.yaw) * np.sin(-self.pitch), np.cos(-self.yaw) * np.cos(-self.pitch)])
        ])
        self.rotation_y_matrix = np.array([
            np.array([np.cos(-self.yaw), 0, np.sin(-self.yaw)]),
            np.array([0, 1, 0]),
            np.array([-np.sin(-self.yaw), 0, np.cos(-self.yaw)])
        ])
        self.right = np.matmul(self.rotation_matrix, np.array((1., 0., 0.)))
        self.forward = np.matmul(self.rotation_y_matrix, np.array((0., 0., -1.)))
