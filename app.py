import streamlit as st
from datasets import load_from_disk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import nltk
nltk.download('punkt')

# Load the dataset from disk
dataset = load_from_disk("pubmed-summarization")

# Predefined function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\[[^]]*\]', '', text)  # Remove citations
    text = text.lower()  # Convert to lowercase
    return text

def summarize_text(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])

st.title("PubMed Article Summarizer")

uploaded_file = st.file_uploader("Upload a PubMed Article", type=["txt"])

if uploaded_file is not None:
    article = uploaded_file.read().decode("utf-8")
    preprocessed_article = preprocess_text(article)
    summary = summarize_text(preprocessed_article)
    
    st.subheader("Original Article")
    st.write(article)
    
    st.subheader("Summarized Article")
    st.write(summary)