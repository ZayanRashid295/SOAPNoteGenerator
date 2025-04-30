from typing import List, Dict
import re

def compare_soap_notes(soap_notes: Dict[str, str]) -> Dict:
    if not soap_notes:
        raise ValueError("No SOAP notes provided for comparison")

    scores = {
        'completeness': [],
        'clarity': [],
        'relevance': []
    }

    notes = list(soap_notes.values())
    api_names = list(soap_notes.keys())

    for note in notes:
        if not isinstance(note, str) or not note.strip():
            continue

        completeness_score = evaluate_completeness(note)
        clarity_score = evaluate_clarity(note)
        relevance_score = evaluate_relevance(note)

        scores['completeness'].append(completeness_score)
        scores['clarity'].append(clarity_score)
        scores['relevance'].append(relevance_score)

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
    sections = {
        'S': r'(?i)subjective:?.*?(?=(objective:|assessment:|plan:|$))',
        'O': r'(?i)objective:?.*?(?=(assessment:|plan:|$))',
        'A': r'(?i)assessment:?.*?(?=(plan:|$))',
        'P': r'(?i)plan:?.*?(?=$)'
    }
    
    score = 0
    for section, pattern in sections.items():
        matches = re.findall(pattern, note, re.DOTALL)
        if matches and any(m.strip() for m in matches):
            score += 25
    return score

def evaluate_clarity(note: str) -> int:
    sentences = re.split(r'[.!?]+', note)
    avg_words_per_sentence = sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0
    return min(100, int(100 * (1 - abs(15 - avg_words_per_sentence) / 15)))

def evaluate_relevance(note: str) -> int:
    keywords = ['symptoms', 'diagnosis', 'treatment', 'medication', 'follow-up',
                'vital signs', 'medical history', 'chief complaint']
    score = 0
    note_lower = note.lower()
    for keyword in keywords:
        if keyword in note_lower:
            score += 12.5
    return min(100, score)

def merge_soap_notes(soap_notes: Dict[str, str]) -> str:
    """
    Merge the best sections from multiple SOAP notes into a single final SOAP note.
    """
    sections = {
        'S': r'(?i)subjective:?.*?(?=(objective:|assessment:|plan:|$))',
        'O': r'(?i)objective:?.*?(?=(assessment:|plan:|$))',
        'A': r'(?i)assessment:?.*?(?=(plan:|$))',
        'P': r'(?i)plan:?.*?(?=$)'
    }
    
    merged_sections = {key: "" for key in sections.keys()}
    
    for note in soap_notes.values():
        for section, pattern in sections.items():
            matches = re.findall(pattern, note, re.DOTALL)
            if matches:
                content = max(matches, key=len).strip()  # Choose the longest match
                if len(content) > len(merged_sections[section]):  # Keep the most detailed section
                    merged_sections[section] = content
    
    final_soap_note = "\n\n".join(
        f"{section}: {content}" for section, content in merged_sections.items() if content
    )
    return final_soap_note