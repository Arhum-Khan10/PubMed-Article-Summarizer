# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datasets import load_from_disk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import nltk
import requests
from rouge import Rouge  

# Download the Punkt tokenizer
nltk.download('punkt')

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "my_secret_key"    

# Load the dataset from disk
dataset = load_from_disk("pubmed-summarization")

# Define hardcoded usernames and passwords
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
}


# Preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\[[^]]*\]', '', text)  # Remove citations
    text = text.lower()  # Convert to lowercase
    return text


# Function to calculate ROUGE scores
def calculate_rouge_scores(summary, reference):
    rouge = Rouge()
    scores = rouge.get_scores(summary, reference)
    return scores


# Function to summarize text and calculate ROUGE scores (brief)
def summarize_text_brief_with_metrics(text, reference, num_sentences=17):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    summary_text = ' '.join([str(sentence) for sentence in summary])
    
    rouge_scores = calculate_rouge_scores(summary_text, reference)
    
    return summary_text, rouge_scores


# Function to summarize text and calculate ROUGE scores (detailed)
def summarize_text_detailed_with_metrics(text, reference, num_sentences=25):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    summary_text = ' '.join([str(sentence) for sentence in summary])
    

    rouge_scores = calculate_rouge_scores(summary_text, reference)
    
    return summary_text, rouge_scores

# Function to authenticate users
def authenticate(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    return False

# Endpoint to retrieve article titles for dropdown
@app.route('/get_articles', methods=['GET'])
def get_articles():
    article_titles = [f"Article {i+1}" for i in range(25)]  
    return jsonify(article_titles)


# Function to summarize text using Gemini API
def summarize_with_gemini(text, api_key):
    url = "https://api.gemini.com/summarize"  
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("summary", "No summary available.")
    else:
        return "Error in summarizing with Gemini."


# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            flash(f"Logged in as {username}", 'success')
            return redirect(url_for('main_app'))
        else:
            flash("Invalid credentials. Please try again.", 'error')
    return render_template('login.html')

# Main app route
@app.route('/main_app', methods=['GET', 'POST'])
def main_app():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        selected_article_index = request.form.get('article')  
        summary_type = request.form.get('summary_type')  

        if uploaded_file or selected_article_index is not None:
            if uploaded_file:
                article = uploaded_file.read().decode("utf-8")
                preprocessed_article = preprocess_text(article)
                reference = article  
                if summary_type == 'brief':
                    summary, rouge_scores = summarize_text_brief_with_metrics(preprocessed_article, reference)
                elif summary_type == 'detailed':
                    summary, rouge_scores = summarize_text_detailed_with_metrics(preprocessed_article, reference)
                return render_template('main_app.html', article=article, summary=summary, rouge_scores=rouge_scores)
            elif selected_article_index is not None:
                article_index = int(selected_article_index)
                selected_article = dataset['train'][article_index]['article']  
                preprocessed_article = preprocess_text(selected_article)
                reference = selected_article  
                if summary_type == 'brief':
                    summary, rouge_scores = summarize_text_brief_with_metrics(preprocessed_article, reference)
                elif summary_type == 'detailed':
                    summary, rouge_scores = summarize_text_detailed_with_metrics(preprocessed_article, reference)
                return render_template('main_app.html', article=selected_article, summary=summary, rouge_scores=rouge_scores)

        flash("Please select an article or upload a file.", 'error')
    
    return render_template('main_app.html')


# AI summarization route
@app.route('/ai_summarizer', methods=['GET', 'POST'])
def ai_summarizer():
    if request.method == 'POST':
        selected_article_index = request.form.get('article')  

        if selected_article_index is not None:
            article_index = int(selected_article_index)
            selected_article = dataset['train'][article_index]['article']  
            preprocessed_article = preprocess_text(selected_article)
            api_key = "AIzaSyBv0qLCjmsgdMxxiNmahFyLIlRr59XbpFQ"  
            summary = summarize_with_gemini(preprocessed_article, api_key)
            return render_template('ai_summarizer.html', article=selected_article, summary=summary)

        flash("Please select an article.", 'error')
    
    return render_template('ai_summarizer.html')


if __name__ == '__main__':
    app.run(debug=True)