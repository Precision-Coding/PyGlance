import numpy as np
import pygame as py

class Camera():
    def __init__(self):
        self.position_vector = np.array([0., -250., 0.])
        self.direction_vector = np.array([0., 1., 0.])
        self.direction_vector_right = np.array([1., 0., 0.])
        self.direction_vector_up = np.array([0., 0., -1.])
        self.fov = np.pi/3
        r = self.direction_vector
        #r.n=k (clipping plane definition)
        self.k = np.dot(self.position_vector+self.direction_vector, self.direction_vector) #Plane positioned 1 unit in front of camera
        self.left_bounding_box = r*np.cos(self.fov/2) + np.cross(r, self.direction_vector_up)*np.sin(self.fov/2) + self.direction_vector_up*np.dot(self.direction_vector_up, r)*(1-np.cos(self.fov/2))
        self.right_bounding_box = r*np.cos(self.fov/2) + np.cross(r, -self.direction_vector_up)*np.sin(self.fov/2) + -self.direction_vector_up*np.dot(-self.direction_vector_up, r)*(1-np.cos(self.fov/2))
        self.top_bounding_box = r*np.cos(self.fov/2) + np.cross(r, self.direction_vector_right)*np.sin(self.fov/2) + self.direction_vector_right*np.dot(self.direction_vector_right, r)*(1-np.cos(self.fov/2))
        self.bottom_bounding_box = r*np.cos(self.fov/2) + np.cross(r, -self.direction_vector_right)*np.sin(self.fov/2) + -self.direction_vector_right*np.dot(-self.direction_vector_right, r)*(1-np.cos(self.fov/2))
        t_horizontal = -(np.dot(self.direction_vector, self.position_vector)-self.k)/np.dot(self.direction_vector, self.left_bounding_box)
        self.left_bounding_coordinate = self.position_vector + t_horizontal*self.left_bounding_box
        self.right_bounding_coordinate = self.position_vector + t_horizontal*self.right_bounding_box
        t_vertical = -(np.dot(self.direction_vector, self.position_vector)-self.k)/np.dot(self.direction_vector, self.bottom_bounding_box)
        self.bottom_bounding_coordinate = self.position_vector + t_vertical*self.bottom_bounding_box
        self.top_bounding_coordinate = self.position_vector + t_vertical*self.top_bounding_box
