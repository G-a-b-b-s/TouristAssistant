import numpy as np
from typing import List

from PointOfInterest import POI
from Graph import Graph, geodistance

class Itinerary:
    daily_pois: List[List[POI]]

    def __init__(self, pois: List[POI], num_of_days: int, num_of_iterations=100, atol=1e-4):
        data = np.array([[x.latitude, x.longitude] for x in pois])
        indices = np.random.choice(data.shape[0], num_of_days, replace=False)
        centers = data[indices]

        for _ in range(num_of_iterations):
            distances = [
                [geodistance(point[0], point[1], center[0], center[1])
                for center in centers]
                for point in data]
            labels = np.argmin(distances, axis=1)
            new_centers = np.array([data[labels == k].mean(axis=0) for k in range(num_of_days)])
            if np.allclose(new_centers, centers, atol=atol):
                break
            centers = new_centers
        
        initial_daily_pois = [[] for _ in range(num_of_days)]
        for i in range(data.shape[0]):
            initial_daily_pois[labels[i]].append(pois[i])
        
        optimal_daily_pois = []
        for x in initial_daily_pois:
            graph = Graph(x)
            path = graph.optimal_path(0)
            optimal_daily_pois.append(path)
        
        self.daily_pois = optimal_daily_pois
    
    def __repr__(self):
        result = ""
        for i, pois in enumerate(self.daily_pois):
            result += f"Day {i + 1}:\n"
            for i, poi in enumerate(pois):
                result += f"{i + 1}. {poi.name}.\n"
        return result.strip()
