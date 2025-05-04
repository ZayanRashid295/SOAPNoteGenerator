from typing import Dict
from collections import defaultdict

def generate_explanation(soap_notes: Dict[str, str], best_soap_note: str, scores: Dict[str, float]) -> str:
    overlap_analysis = find_overlapping_points(soap_notes)
    
    explanation = "SOAP Notes Analysis Report\n\n"
    explanation += "Common Points Analysis:\n"
    
    if any(color == "red" for color in overlap_analysis.values()):
        explanation += "\nPoints present in all 4 SOAP notes (High Confidence):\n"
        for point, color in overlap_analysis.items():
            if color == "red":
                explanation += f"- {point}\n"
    
    if any(color == "green" for color in overlap_analysis.values()):
        explanation += "\nPoints present in 3 SOAP notes (Medium Confidence):\n"
        for point, color in overlap_analysis.items():
            if color == "green":
                explanation += f"- {point}\n"
    
    if any(color == "yellow" for color in overlap_analysis.values()):
        explanation += "\nPoints present in 2 SOAP notes (Low Confidence):\n"
        for point, color in overlap_analysis.items():
            if color == "yellow":
                explanation += f"- {point}\n"

    return explanation

def find_overlapping_points(soap_notes: Dict[str, str]) -> Dict[str, str]:
    all_points = defaultdict(int)
    
    for note in soap_notes.values():
        sentences = [s.strip().lower() for s in note.split('.') if s.strip()]
        for sentence in sentences:
            all_points[sentence] += 1
    
    overlap_analysis = {}
    for point, count in all_points.items():
        if count == 4:
            overlap_analysis[point] = "red"
        elif count == 3:
            overlap_analysis[point] = "green"
        elif count == 2:
            overlap_analysis[point] = "yellow"
    
    return overlap_analysis