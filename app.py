import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from utils import (
    analyze_essay,
    generate_feedback,
    extract_keywords,
    generate_smart_feedback,
    generate_summary,
    generate_pdf_report
)

st.set_page_config(page_title="AI Tutor Assistant", layout="wide")
st.title("🎓 AI Tutor Assistant")
import streamlit as st
import os

#  OpenRouter API key securely
api_key = st.secrets["OPENROUTER_API_KEY"]


# Toggle smart GPT-style feedback
use_smart = st.checkbox(" Use GPT-style Smart Feedback", value=True)

# Upload essays file: accepts CSV or TXT
uploaded_file = st.file_uploader(
    " Upload a CSV file with an 'essay' column",
    type=["csv", "txt"],
    key="essay_upload"
)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        st.error(" Could not read file. Please upload a CSV with an 'essay' column.")
        st.stop()

    if 'essay' not in df.columns:
        st.error(" CSV must contain an 'essay' column.")
        st.stop()

    results = []
    sentiments = []

    for i, row in df.iterrows():
        text = row['essay']

        # Get sentiment label and confidence (3-class model: POSITIVE, NEUTRAL, NEGATIVE)
        sentiment, confidence = analyze_essay(text)

        # Generate feedback: smart GPT or classic
        if use_smart:
            feedback = generate_smart_feedback(text, api_key)
        else:
            feedback = generate_feedback(text)

        # Extract keywords
        keywords = extract_keywords(text)
        sentiment_label = sentiment.split()[0]  # Just POSITIVE, NEUTRAL, or NEGATIVE
        sentiments.append(sentiment_label)

        results.append({
            "essay": text,
            "sentiment": sentiment_label,
            "confidence": confidence,
            "keywords": ", ".join(keywords),
            "feedback": feedback
        })

    if results:
        result_df = pd.DataFrame(results)

        # --- Sentiment Filter UI ---
        sentiment_filter = st.multiselect(
            "Filter essays by sentiment:",
            options=["POSITIVE", "NEUTRAL", "NEGATIVE"],
            default=["POSITIVE", "NEUTRAL", "NEGATIVE"]
        )

        # Filter dataframe based on sentiment selection
        filtered_df = result_df[result_df['sentiment'].isin(sentiment_filter)]

        # --- Search filter ---
        search_text = st.text_input("🔍 Search essays (filter by text):").strip().lower()
        if search_text:
            filtered_df = filtered_df[
                filtered_df['essay'].str.lower().str.contains(search_text) |
                filtered_df['feedback'].str.lower().str.contains(search_text) |
                filtered_df['keywords'].str.lower().str.contains(search_text)
            ]

        st.write(f" **Feedback Table ({len(filtered_df)} essays shown)**")
        st.dataframe(filtered_df)

        # Save full output CSV (unfiltered)
        result_df.to_csv("results/feedback_output.csv", index=False)
        st.success(" Analysis complete! Output saved to results/feedback_output.csv")

        # Plot sentiment distribution for filtered data
        st.subheader(" Sentiment Distribution")
        sentiment_counts = pd.Series(filtered_df['sentiment']).value_counts()
        fig, ax = plt.subplots()
        sentiment_counts.plot(kind='bar', color=['green', 'gray', 'red'], ax=ax)
        ax.set_xlabel("Sentiment")
        ax.set_ylabel("Number of Essays")
        ax.set_title("Distribution of Essay Sentiments (Filtered)")
        st.pyplot(fig)

        # --- Pie Chart ---
        fig2, ax2 = plt.subplots()
        colors = {
            "POSITIVE": "green",
            "NEGATIVE": "red",
            "NEUTRAL": "gray"
        }
        labels = sentiment_counts.index.tolist()
        sizes = sentiment_counts.values.tolist()
        pie_colors = [colors.get(label, "blue") for label in labels]

        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=pie_colors)
        ax2.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
        st.pyplot(fig2)

        # Overall summary using smart GPT only if API key is set
        st.subheader(" Overall Summary of Student Feedback")
        if api_key and api_key.startswith("sk-or"):
            summary = generate_summary(filtered_df['feedback'].tolist(), api_key)
            st.info(summary)
        else:
            st.warning(" API key missing or invalid, cannot generate overall summary.")

        # PDF report download (for filtered data)
        pdf_path = generate_pdf_report(filtered_df)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=" Download Full Feedback Report (PDF)",
                data=f,
                file_name="feedback_report.pdf",
                mime="application/pdf"
            )
