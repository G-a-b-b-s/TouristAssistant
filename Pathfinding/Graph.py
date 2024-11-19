from numpy import cos, sqrt
from typing import List

from PointOfInterest import POI

def geodistance(lat1, lon1, lat2, lon2):
    lat_diff = lat1 - lat2
    lon_diff = lon1 - lon2
    mean_lat = (lat1 + lat2) / 2
    cmp = lat_diff ** 2 + (lon_diff * cos(mean_lat)) ** 2
    R = 6371009
    return R * sqrt(cmp)

class Graph:
    vertices: List[POI]
    matrix: List[List[float]]

    def __init__(self, vertices: List[POI], matrix: List[List[float]] = None):
        self.vertices = vertices

        if matrix:
            self.matrix = matrix
        else:
            self.matrix = [[geodistance(v1.latitude, v1.longitude, v2.latitude, v2.longitude)
                        for v2 in vertices]
                        for v1 in vertices]

    def optimal_path(self, start: int) -> List[POI]:
        mst = self.MST()
        initial_path = self.find_path(mst, start)
        best_path = self.optimize_path(initial_path)
        return [self.vertices[v] for v in best_path]

    def path_distance(self, path: List[int]):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.matrix[path[i]][path[i + 1]]
        return distance

    def MST(self) -> List[List[int]]:
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

        return mst

    def find_path(self, mst: List[List[int]], start: int) -> List[int]:
        n = len(self.matrix)
        path = []

        def DFS(v1):
            for v2 in range(n):
                if mst[v1][v2] != 0:
                    mst[v1][v2] = 0
                    DFS(v2)

            if set(range(n)) - set(path):
                path.append(v1)

        DFS(start)
        return path

    def optimize_path(self, initial_path: List[int]) -> List[int]:
        best_path = initial_path
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

        return result