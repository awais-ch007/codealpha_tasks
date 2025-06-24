
import language_tool_python
from sentence_transformers import SentenceTransformer, util
import textstat
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import numpy as np

nltk.download('punkt')

# Initialize tools
tool = language_tool_python.LanguageTool('en-US')
model = SentenceTransformer('all-MiniLM-L6-v2')  # Light and fast embedding model

# Reference prompt for content relevance
reference_prompt = "Discuss the impact of climate change on global agriculture and suggest potential solutions."

def grammar_score(essay):
    matches = tool.check(essay)
    num_errors = len(matches)
    total_words = len(word_tokenize(essay))
    score = max(0, 100 - (num_errors / max(1, total_words)) * 100)  # Penalty for error density
    return round(score, 2), num_errors

def content_relevance_score(essay, reference):
    essay_embedding = model.encode(essay, convert_to_tensor=True)
    ref_embedding = model.encode(reference, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(essay_embedding, ref_embedding).item()
    return round(similarity * 100, 2)  # Scale to 0–100

def readability_score(essay):
    return textstat.flesch_reading_ease(essay)

def vocabulary_richness(essay):
    words = word_tokenize(essay.lower())
    total_words = len(words)
    unique_words = len(set(words))
    return round((unique_words / max(1, total_words)) * 100, 2)

def overall_score(grammar, content, readability, vocab):
    # Weighted average: grammar (30%), content (30%), readability (20%), vocabulary (20%)
    return round((grammar * 0.3) + (content * 0.3) + (readability * 0.2) + (vocab * 0.2), 2)

def analyze_essay(essay, prompt):
    grammar, num_errors = grammar_score(essay)
    content = content_relevance_score(essay, prompt)
    readability = readability_score(essay)
    vocab = vocabulary_richness(essay)
    final = overall_score(grammar, content, readability, vocab)

    return {
        "Grammar Score": grammar,
        "Grammar Errors": num_errors,
        "Content Relevance": content,
        "Readability": readability,
        "Vocabulary Richness": vocab,
        "Overall Score": final
    }

# === Example Usage ===
essay_text = """
Climate change has drastically altered weather patterns across the globe. This has impacted agriculture through droughts, floods, and unpredictable seasons. 
To mitigate these effects, sustainable farming, climate-resilient crops, and policy changes are needed.
"""

results = analyze_essay(essay_text, reference_prompt)
for k, v in results.items():
    print(f"{k}: {v}")