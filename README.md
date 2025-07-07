# 📚 AI Tutor Assistant

**AI Tutor Assistant** is a Streamlit web application that analyzes student essays for sentiment and provides both classic and GPT-enhanced feedback. Designed for educators and learners, this tool makes it easy to understand student writing at scale and give actionable, personalized insights.



##  Features

  Upload CSV files with an `essay` column
 Multi-class sentiment analysis: **Positive 😊**, **Neutral 😐**, **Negative 😠**
 Keyword extraction from each essay
 Two feedback modes:
   Classic rule-based feedback
   GPT-style smart feedback (optional)
-Visualize sentiment distribution (bar and pie charts)
 Filter by sentiment type and search specific essays
 Download full feedback report as a **PDF**
 GPT-generated overall summary of all essays (optional)



## Getting Started

###  Prerequisites

Python 3.8 or higher
 pip (Python package manager)
 (Optional) OpenAI API key for GPT feedback

###  Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ai-tutor-assistant.git
   cd ai-tutor-assistant

   # Create venv
python -m venv venv

# On Windows
.\venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate


Install dependencies
pip install -r requirements.txt
The following Python packages are required:
streamlit
pandas
matplotlib
seaborn
nltk
openai
scikit-learn
fpdf

Run the Streamlit app
streamlit run app.py
or
python -m streamlit run app.py


