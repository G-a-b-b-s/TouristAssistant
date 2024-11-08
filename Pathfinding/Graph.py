import math
from typing import Self, List, Set

from PointOfInterest import POI

def distance(v1: POI, v2: POI):
    latitude_diff = v1.latitude - v2.latitude
    longitude_diff = v1.longitude - v2.longitude
    mean_latitude = (v1.latitude + v2.latitude) / 2
    cmp = latitude_diff ** 2 + (longitude_diff * math.cos(mean_latitude)) ** 2
    R = 6371009
    return R * math.sqrt(cmp)

class Graph:
    def __init__(self, vertices: List[POI]):
        self.vertices = vertices
        self.matrix = [[distance(v1, v2) for v2 in vertices] for v1 in vertices]

    def MST(self) -> Self:
        mst = Graph(self.vertices)
        num_of_vertices = len(self.vertices)

        covered: Set[int] = {0}
        not_covered: Set[int] = set([x for x in range(1, num_of_vertices)])
        edges: Set[(int, int)] = set()

        while not_covered:
            min: float = float('inf')
            selected_vertix: int
            previous_vertix: int

            for i in covered:
                for j in not_covered:
                    d = self.matrix[i][j]
                    if d <= min:
                        min = d
                        selected_vertix = j
                        previous_vertix = i

            not_covered.remove(selected_vertix)
            covered.add(selected_vertix)
            edges.add((selected_vertix, previous_vertix))
        
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices)):
                if (i, j) not in edges and (j, i) not in edges: 
                    mst.matrix[i][j] = 0
        return mst

pois = [
    POI('first', 'castle', 37.7749, -122.4194, {}),
    POI('second', 'castle', 37.7753, -122.4187, {}),
    POI('third', 'castle', 37.7745, -122.4200, {}),
    POI('fourth', 'restaurant', 37.7741, -122.4198, {}),
    POI('fifth', 'idk', 37.7750, -122.4202, {})
]
graph = Graph(pois)
graph.MST()