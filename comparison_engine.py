from typing import List, Dict
import re
from collections import Counter, defaultdict

def compare_soap_notes(soap_notes: Dict[str, str]) -> Dict:
    if not soap_notes:
        raise ValueError("No SOAP notes provided for comparison")

    scores = {'completeness': [], 'clarity': [], 'relevance': []}
    notes = list(soap_notes.values())
    api_names = list(soap_notes.keys())

    for note in notes:
        if not isinstance(note, str) or not note.strip():
            continue
        scores['completeness'].append(evaluate_completeness(note))
        scores['clarity'].append(evaluate_clarity(note))
        scores['relevance'].append(evaluate_relevance(note))

    if not scores['completeness']:
        raise ValueError("No valid SOAP notes to compare")

    total_scores = [
        (0.4 * scores['completeness'][i] +
         0.3 * scores['clarity'][i] +
         0.3 * scores['relevance'][i])
        for i in range(len(notes))
    ]
    best_score_index = total_scores.index(max(total_scores))

    return {
        'best_soap_note': notes[best_score_index],
        'scores': {
            'completeness': scores['completeness'][best_score_index],
            'clarity': scores['clarity'][best_score_index],
            'relevance': scores['relevance'][best_score_index],
            'total': total_scores[best_score_index]
        },
        'api_used': api_names[best_score_index]
    }

def evaluate_completeness(note: str) -> int:
    sections = ['subjective', 'objective', 'assessment', 'plan']
    score = sum(25 for section in sections if re.search(fr'(?i){section}:?.*?(?=(objective:|assessment:|plan:|$))', note, re.DOTALL))
    return score

def evaluate_clarity(note: str) -> int:
    sentences = re.split(r'[.!?]+', note)
    avg_words = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    return min(100, int(100 * (1 - abs(15 - avg_words) / 15)))

def evaluate_relevance(note: str) -> int:
    keywords = ['symptoms', 'diagnosis', 'treatment', 'medication', 'follow-up',
                'vital signs', 'medical history', 'chief complaint']
    return min(100, sum(12.5 for keyword in keywords if keyword in note.lower()))

def merge_soap_notes(soap_notes: Dict[str, str]) -> str:
    all_sections = defaultdict(list)
    for note in soap_notes.values():
        for section, content in extract_sections(note).items():
            if content:
                all_sections[section].append(content)

    merged_note = ""
    for section, contents in all_sections.items():
        unique_points = set(point.strip() for content in contents for point in content.split('.') if point.strip())
        merged_note += f"\n{section}:\n" + ". ".join(sorted(unique_points)) + ".\n"
    return merged_note.strip()

def extract_sections(note: str) -> Dict[str, str]:
    patterns = {
        'Subjective': r'(?i)subjective:?(.*?)(?=objective:|assessment:|plan:|$)',
        'Objective': r'(?i)objective:?(.*?)(?=assessment:|plan:|$)',
        'Assessment': r'(?i)assessment:?(.*?)(?=plan:|$)',
        'Plan': r'(?i)plan:?(.*?)$'
    }
    return {section: (re.search(pattern, note, re.DOTALL).group(1).strip() if re.search(pattern, note, re.DOTALL) else '') for section, pattern in patterns.items()}

def identify_overlapping_points(outputs: Dict[str, str]) -> Dict[str, str]:
    all_points = Counter(point for output in outputs.values() for point in output.splitlines())
    return {point: "red" if count == 4 else "green" if count == 3 else "yellow" for point, count in all_points.items() if count >= 2}