# utils.py

import os
import re
import uuid
import unicodedata
from fpdf import FPDF
from sklearn.feature_extraction.text import CountVectorizer

# Dummy sentiment analyzer (replace with real model or API)
# Smarter placeholder sentiment analyzer


def analyze_essay(text):
    text_lower = text.lower()

    positive_keywords = [
        "well done", "good", "excellent", "great", "improved", "outstanding",
        "strong", "clear", "insightful", "creative", "amazing", "brilliant",
        "fantastic", "very well", "impressive", "logical", "coherent", "successful"
    ]

    negative_keywords = [
        "bad", "poor", "confusing", "terrible", "weak", "needs work", "incomplete",
        "unclear", "lacking", "problem", "incorrect", "disorganized", "irrelevant"
    ]

    pos_hits = [kw for kw in positive_keywords if kw in text_lower]
    neg_hits = [kw for kw in negative_keywords if kw in text_lower]

    pos_score = len(pos_hits)
    neg_score = len(neg_hits)

    print(f"[DEBUG] POSITIVE hits: {pos_hits}")
    print(f"[DEBUG] NEGATIVE hits: {neg_hits}")

    if pos_score > neg_score:
        return "POSITIVE 😊", min(0.90 + 0.02 * pos_score, 0.99)
    elif neg_score > pos_score:
        return "NEGATIVE 😠", min(0.90 + 0.02 * neg_score, 0.99)
    else:
        return "NEUTRAL 😐", 0.75

    
    

# Extract keywords using basic count vectorizer
def extract_keywords(text, top_n=5):
    vectorizer = CountVectorizer(stop_words="english", max_features=top_n)
    X = vectorizer.fit_transform([text])
    return vectorizer.get_feature_names_out()

# Basic rule-based feedback generator
def generate_feedback(text):
    return "This essay covers some key points. Consider expanding on your arguments and structuring your ideas more clearly."

# Smart GPT-style feedback (placeholder logic)
def generate_smart_feedback(text, api_key):
    return "[GPT] Your essay demonstrates strong understanding. However, make sure to support your claims with evidence."

# Smart summary of feedback list
def generate_summary(feedback_list, api_key):
    combined = " ".join(feedback_list)
    return "Overall, the students generally showed understanding, but there is room for improvement in structure, clarity, and evidence use."

# Helper to clean text for PDF compatibility
def clean_text(text):
    """Remove or replace characters that can't be encoded in Latin-1."""
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKD', text)
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r'[^\x00-\xFF]', '', text)
    return text

# PDF report generation
def generate_pdf_report(df, output_path="results"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = f"feedback_report_{uuid.uuid4().hex[:6]}.pdf"
    filepath = os.path.join(output_path, filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, clean_text("AI Tutor Assistant Feedback Report"), ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)

    for idx, row in df.iterrows():
        essay = clean_text(row.get('essay', '')[:1000])
        sentiment = clean_text(row.get('sentiment', ''))
        confidence = row.get('confidence', 0.0)
        keywords = clean_text(row.get('keywords', ''))
        feedback = clean_text(row.get('feedback', ''))

        pdf.multi_cell(0, 10, f"Essay {idx + 1}:\n", align="L")
        pdf.set_font("Arial", style="I", size=11)
        pdf.multi_cell(0, 8, essay + "\n", align="L")
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Sentiment: {sentiment}   | Confidence: {confidence:.2f}", ln=True)
        pdf.cell(0, 8, f"Keywords: {keywords}", ln=True)
        pdf.multi_cell(0, 8, f"Feedback: {feedback}", align="L")
        pdf.ln(5)

    pdf.output(filepath)
    return filepath
