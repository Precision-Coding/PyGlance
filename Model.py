from STLParser import parseStl
from Polygon import Polygon
import numpy as np

class Model():
    def __init__(self):
        self.raw_array = parseStl("STLFiles/CatLowPoly.stl")
        self.colour = np.array((200, 0, 200))
        self.polygon_array = self.polygonConverter()
        self.pitch = 0
        self.yaw = 0.05
        self.roll = 0

    def polygonConverter(self):
        translation = np.array((0, 0, -50))
        data = self.raw_array
        polygons = []
        for tuple in data:
            polygon = Polygon(normal=np.array(tuple[0]), vertices_coordinates=np.array(tuple[1:])+translation)
            polygons.append(polygon)
        return polygons