from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datasets import load_from_disk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import re
import nltk

nltk.download('punkt')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure value

# Load the dataset from disk
dataset = load_from_disk("pubmed-summarization")

# Predefined function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    text = re.sub(r'\[[^]]*\]', '', text)  # Remove citations
    text = text.lower()  # Convert to lowercase
    return text

# Function to summarize text (brief)
def summarize_text_brief(text, num_sentences=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])

# Function to summarize text (detailed)
def summarize_text_detailed(text, num_sentences=10):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join([str(sentence) for sentence in summary])

# Endpoint to retrieve article titles for dropdown
@app.route('/get_articles', methods=['GET'])
def get_articles():
    # Fetch titles from the first 10 articles in the 'train' section of the dataset
    article_titles = [f"Article {i+1}" for i in range(10)]  
    return jsonify(article_titles)

# Define hardcoded usernames and passwords
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2"
}

# Function to authenticate users
def authenticate(username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        return True
    return False

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
        selected_article_index = request.form.get('article')  # Get selected article index from dropdown
        summary_type = request.form.get('summary_type')  # Get selected summary type

        if uploaded_file or selected_article_index is not None:
            if uploaded_file:
                article = uploaded_file.read().decode("utf-8")
                preprocessed_article = preprocess_text(article)
                if summary_type == 'brief':
                    summary = summarize_text_brief(preprocessed_article)
                elif summary_type == 'detailed':
                    summary = summarize_text_detailed(preprocessed_article)
                return render_template('main_app.html', article=article, summary=summary)
            elif selected_article_index is not None:
                article_index = int(selected_article_index)
                selected_article = dataset['train'][article_index]['article']  # Correctly access the article's text
                preprocessed_article = preprocess_text(selected_article)
                if summary_type == 'brief':
                    summary = summarize_text_brief(preprocessed_article)
                elif summary_type == 'detailed':
                    summary = summarize_text_detailed(preprocessed_article)
                return render_template('main_app.html', article=selected_article, summary=summary)

        flash("Please select an article or upload a file.", 'error')
    
    return render_template('main_app.html')

if __name__ == '__main__':
    app.run(debug=True)