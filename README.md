# PubMed-Article-Summarizer
This repository contains a Flask-based web application for summarizing PubMed articles. The application allows users to upload articles or select from preloaded articles, preprocesses the text, generates summaries using the Latent Semantic Analysis (LSA) method, and calculates ROUGE scores to evaluate the quality of the summaries.
## Dependencies:
To run the PubMed Article Summarizer, you'll need the following dependencies:
- Python 3.7+
- Flask
- Hugging Face Datasets
- Sumy
- NLTK
- Rouge
- Requests

## Installation:
1. Clone the repository from GitHub using
    - ```git clone https://github.com/your-username/pubmed-article-summarizer.git```
    - ```cd pubmed-article-summarizer```
2. Install all the libraries by running the following command on the cmd or terminal
    - ```pip install flask datasets sumy nltk rouge-score requests```

## Features
### Efficient Text Preprocessing
   - Text Cleaning: Removes extra spaces, citations, and converts text to lowercase.
### Summarization
   - Latent Semantic Analysis (LSA) Summarizes text using LSA with options for brief or detailed summaries.
Quality Evaluation
   - ROUGE Scores: Calculates ROUGE scores to evaluate the quality of the summaries.

## How to Use
1. #### Setup
  - Start the flask application by running the following command on your cmd or terminal:
    - ```python app.py```
2. #### Login
  - Access the web application at http://127.0.0.1:5000/.
  - Use one of the predefined usernames and passwords to log in.
3. #### Upload or Select an article
  - Upload a PubMed article in text format.
  - Or, select an article from the preloaded dataset using the dropdown menu.

### Main Application
- Summarize: Choose the type of summary (brief or detailed) and view the original and summarized articles along with the ROUGE scores.

### User Authentication
- The application includes a simple user authentication mechanism with predefined usernames and passwords.

### Detailed Code Explanation
### Login Route
  - Handles user login with predefined credentials.
  - Redirects authenticated users to the main application page.
### Main Application Route
  - Allows users to upload an article or select from preloaded articles.
  - Preprocesses the text and generates summaries using LSA.
  - Calculates and displays ROUGE scores to evaluate the summaries.
### Utility Functions
  - preprocess_text: Cleans and preprocesses the input text.
  - summarize_text_brief_with_metrics: Generates brief summaries and calculates ROUGE scores.
  - summarize_text_detailed_with_metrics: Generates detailed summaries and calculates ROUGE scores.
## Usage

### Data Preprocessing:
  - The application preprocesses uploaded or selected articles by removing extra spaces and citations and converting text to lowercase.

### Summarization:
  - Generate brief or detailed summaries using the LSA method.

### Quality Evaluation:
  - The application calculates ROUGE scores to evaluate the quality of the generated summaries against the original articles.

## Why Choose Our Solution
  - Scalability: Built with Flask, allowing easy deployment and scaling.
  - Accuracy: Utilizes LSA and ROUGE scores to ensure high-quality summaries.
  - User-Friendly: Simple web interface for uploading/selecting articles and viewing summaries.

Feel free to contribute to the project by forking the repository and submitting pull requests.
## Contact
For any questions or issues, please contact khanarhum712@gmail.com.

















  
