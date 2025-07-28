import os
import json
import argparse
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence")
    parser.add_argument('--input', required=True, help='Path to challenge1b_input.json')
    parser.add_argument('--pdf_dir', required=True, help='Path to folder containing PDFs')
    parser.add_argument('--output', required=True, help='Path to write challenge1b_output.json')
    return parser.parse_args()


def load_input(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_sections(pdf_path):
    text = extract_text(pdf_path)
    pages = text.split('\f')  # form-feed separates pages
    sections = []
    for i, page in enumerate(pages, start=1):
        lines = [ln.strip() for ln in page.splitlines() if ln.strip()]
        title = lines[0] if lines else f"Page {i}"
        sections.append({
            'page': i,
            'section_title': title,
            'text': ' '.join(lines)
        })
    return sections


def split_sentences(text):
    # Simple sentence splitter
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def main():
    args = parse_args()
    data = load_input(args.input)

    # Input documents list
    docs = data.get('documents', [])
    pdfs = []
    for d in docs:
        fname = d.get('filename')
        path = os.path.join(args.pdf_dir, fname)
        if os.path.isfile(path):
            pdfs.append(path)

    # Extract sections
    all_sections = []
    for pdf in pdfs:
        for sec in extract_sections(pdf):
            all_sections.append({
                'document': os.path.basename(pdf),
                'page': sec['page'],
                'section_title': sec['section_title'],
                'text': sec['text']
            })

    # Build query
    persona_role = data.get('persona', {}).get('role', '')
    job_task = data.get('job_to_be_done', {}).get('task', '')
    query = f"{persona_role} {job_task}".strip()

    # TF-IDF vectorization for sections + query
    texts = [s['text'] for s in all_sections]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(texts + [query])
    sec_vecs = tfidf[:-1]
    query_vec = tfidf[-1]

    # Compute similarities
    sims = cosine_similarity(sec_vecs, query_vec).flatten()
    for sec, score in zip(all_sections, sims):
        sec['score'] = float(score)

    # Rank and take top 5
    ranked = sorted(all_sections, key=lambda x: x['score'], reverse=True)[:5]

    # Prepare extracted sections (top 5)
    extracted_sections = []
    for idx, sec in enumerate(ranked, start=1):
        extracted_sections.append({
            'document': sec['document'],
            'section_title': sec['section_title'],
            'importance_rank': idx,
            'page_number': sec['page']
        })

    # Subsection analysis with TF-IDF sentence scoring
    subsection_analysis = []
    for sec in ranked:
        sentences = split_sentences(sec['text'])
        if sentences:
            sent_vecs = vectorizer.transform(sentences)
            scores = cosine_similarity(sent_vecs, query_vec).flatten()
            # pick top 5 sentences
            top_idxs = scores.argsort()[::-1][:5]
            refined = ' '.join([sentences[i] for i in sorted(top_idxs)])
        else:
            refined = ''
        subsection_analysis.append({
            'document': sec['document'],
            'refined_text': refined,
            'page_number': sec['page']
        })

    # Build output JSON
    output = {
        'metadata': {
            'input_documents': [os.path.basename(p) for p in pdfs],
            'persona': persona_role,
            'job_to_be_done': job_task,
            'processing_timestamp': datetime.utcnow().isoformat() + 'Z'
        },
        'extracted_sections': extracted_sections,
        'subsection_analysis': subsection_analysis
    }

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if _name_ == '_main_':
    main()
