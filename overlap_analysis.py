from collections import Counter
from typing import Dict

def identify_overlapping_points(outputs: Dict[str, str]) -> Dict[str, str]:
    """
    Identifies overlapping points in the outputs and assigns colors based on the number of matches.
    - Red: Points present in all outputs
    - Green: Points present in most outputs (3 out of 4)
    - Yellow: Points present in some outputs (2 out of 4)
    """
    points_by_api = {api: set(output.splitlines()) for api, output in outputs.items()}
    all_points = Counter(point for points in points_by_api.values() for point in points)

    categorized_points = {}
    for point, count in all_points.items():
        if count == len(outputs):  
            categorized_points[point] = "red"
        elif count == len(outputs) - 1:  
            categorized_points[point] = "green"
        elif count == len(outputs) - 2:  
            categorized_points[point] = "yellow"

    return categorized_points
