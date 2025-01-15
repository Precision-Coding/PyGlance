from STLParser import parseStl
from Polygon import Polygon
import numpy as np

class Model():
    def __init__(self):
        self.raw_array = parseStl("STLFiles/TestFile.stl")
        self.polygon_array = self.polygonConverter()
        self.pitch = 0
        self.yaw = np.pi/8
        self.roll = 0

    def polygonConverter(self):
        translation = np.array((100, 0, 0))
        data = self.raw_array
        polygons = []
        for tuple in data:
            polygon = Polygon(normal=np.array(tuple[0]), vertices_coordinates=np.array(tuple[1:]), colour="grey")
            polygons.append(polygon)
        return polygons