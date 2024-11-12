import math
from typing import Self, List, Set
from copy import deepcopy

from PointOfInterest import POI

def distance(v1: POI, v2: POI):
    latitude_diff = v1.latitude - v2.latitude
    longitude_diff = v1.longitude - v2.longitude
    mean_latitude = (v1.latitude + v2.latitude) / 2
    cmp = latitude_diff ** 2 + (longitude_diff * math.cos(mean_latitude)) ** 2
    R = 6371009
    return R * math.sqrt(cmp)

class Graph:
    def __init__(self, vertices: List[POI], matrix: List[List[float]] = None):
        self.vertices = vertices

        if matrix:
            self.matrix = matrix
        else:
            self.matrix = [[distance(v1, v2)
                        for v2 in vertices]
                        for v1 in vertices]

    def MST(self) -> Self:
        n = len(self.vertices)
        mst = [[0 for _ in self.vertices] for _ in self.vertices]

        all_vertices= set(range(n))
        covered = {0}

        while len(covered) != n:
            min = float('inf')
            next_vertix = 0
            previous_vertix = 0

            for v1 in covered:
                for v2 in all_vertices - covered:
                    distance = self.matrix[v1][v2]
                    if distance <= min:
                        min = distance
                        next_vertix = v2
                        previous_vertix = v1

            covered.add(next_vertix)
            mst[next_vertix][previous_vertix] = min
            mst[previous_vertix][next_vertix] = min

        return Graph(self.vertices, mst)
    
    def path_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.matrix[path[i]][path[i + 1]]
        return distance

    def find_path(self, start: int) -> List[POI]:
        n = len(self.matrix)
        edges = deepcopy(self.matrix)
        path = []

        def DFS(v1):
            for v2 in range(n):
                if edges[v1][v2] != 0:
                    edges[v1][v2] = 0
                    DFS(v2)

            if set(range(n)) - set(path):
                path.append(v1)

        DFS(start)
        return [self.vertices[v] for v in path]

    def optimize_path(self, initial_path: List[POI]) -> List[POI]:
        best_path = [self.vertices.index(x) for x in initial_path]
        best_distance = self.path_distance(best_path)
        improved = True

        while improved:
            improved = False
            for i in range(1, len(best_path) - 2):
                for j in range(i + 1, len(best_path) - 1):
                    new_path = best_path[:i] + best_path[i:j+1][::-1] + best_path[j+1:]
                    new_distance = self.path_distance(new_path)

                    if new_distance < best_distance:
                        best_path = new_path
                        best_distance = new_distance
                        improved = True
                        break
                if improved:
                    break
        
        result = [best_path[0]]
        for i in range(1, len(best_path)):
            if best_path[i] != result[-1]:
                result.append(best_path[i])

        return [self.vertices[v] for v in result]

pois = [
    POI('first', 'castle', 37.7749, -122.4194, {}),
    POI('second', 'castle', 37.7753, -122.4187, {}),
    POI('third', 'castle', 37.7745, -122.4200, {}),
    POI('fourth', 'restaurant', 37.7741, -122.4198, {}),
    POI('fifth', 'idk', 37.7750, -122.4202, {})
]
graph = Graph(pois)
mst = graph.MST()
initial_path = mst.find_path(0)
best_path = mst.optimize_path(initial_path)
print(best_path)