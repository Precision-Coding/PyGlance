from STLParser import parseStl
from Polygon import Polygon
import numpy as np

class Model():
    def __init__(self, file_name, offset_vector):
        self.translation_vector = offset_vector
        self.colour = np.array((25, 130, 175))
        self.polygon_array = self.polygonConverter(file_name)
        self.pitch = 0.0
        self.yaw = 0.0
        self.roll = 0.0
        self.translate()

    def polygonConverter(self, file_name):
        polygons = []
        for tuple in parseStl(file_name):
            polygon = Polygon(normal=np.array(tuple[0]), vertices_coordinates=np.array(tuple[1:]))
            polygons.append(polygon)
        return polygons

    def translate(self):
        for polygon in self.polygon_array:
            polygon.vertices_coordinates + self.translation_vector

    def render(self, camera, display):
        #transforms the polygons shades and culls backfacing
        for polygon in self.polygon_array:
            polygon.rotate(self.pitch, self.yaw, self.roll)
            polygon.shade(camera, self.colour)
            polygon.project(camera, display)
            polygon.cull(display)

        #Sorts by distance from camera | draws furthest first
        self.polygon_array = sorted(self.polygon_array, key=lambda polygon: np.linalg.norm(polygon.middle_coordinate-camera.position_vector), reverse=True)