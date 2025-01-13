from STLParser import parseSTL
from Polygon import Polygon
import numpy as np
class Model():
    def __init__(self, display):
        self.rawArray = parseSTL("STLFiles/TestFile.stl")
        self.display = display
        self.PolygonArray = self.polygonConverter()

    def polygonConverter(self):
        data = self.rawArray
        polygons = []
        for touple in data:
            polygon = Polygon(normal=np.array(touple[0]), coordinate1=np.array(touple[1])+np.array((0,50,0)), coordinate2=np.array(touple[2])+np.array((0,50,0)) , coordinate3=np.array(touple[3])+np.array((0,50,0)), colour="grey", display=self.display)
            polygons.append(polygon)
        return polygons